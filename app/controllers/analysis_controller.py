import pandas as pd
from sklearn.linear_model import LinearRegression

class AnalysisController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        
        self.athlete_dao = context.athlete_dao
        self.evaluation_dao = context.evaluation_dao

    def get_all_athletes(self):
        athletes = self.athlete_dao.get_all_athletes()

        return athletes

    def get_evaluation_results(self, athlete_id):
        data = self.evaluation_dao.select_data_for_training("pro")
        df = pd.DataFrame(data)
        df = df.dropna(subset=["result_id"])

        # 1. Cleaning dataset
        df_clean = self.remove_outliers_global(df)
        
        #2. Applying Multiple Regression
        df_final = self.apply_regression(df_clean)

        if(athlete_id):
            return df_final[df_final["athlete_id"] == athlete_id].copy()
        
        return df_final
    
    def apply_regression(self, df):
        df = df.copy()
    
        # Variáveis independentes
        X = df[["dist_center_cm", "angle_norm"]]
        
        # Variável dependente
        y = df["reaction_time"]
        
        # Modelo
        model = LinearRegression()
        model.fit(X, y)

        # Predição do tempo "esperado" dado a dificuldade mecânica
        df["pred_rt"] = model.predict(X)

        # O que sobrou = tempo de reação real
        df["rt_residual"] = y - df["pred_rt"]

        # Tempo ajustado = intercepto + resíduo
        df["reaction_time_adjusted"] = model.intercept_ + df["rt_residual"]

        return df
    
    def compare_adaptive_window(self, df, window_size=5, stable_threshold=3.0):
        """
        Compara duas janelas consecutivas de sessões do atleta (N adaptativo)
        e retorna estatísticas + tendência semântica.
        """

        # Garantir ordem por sessão
        test_ids = sorted(df["test_id"].unique())

        # Precisa de pelo menos 2N sessões
        if len(test_ids) < window_size * 2:
            return None

        # Definição das janelas
        recent_tests = test_ids[-window_size:]
        previous_tests = test_ids[-(window_size * 2):-window_size]

        recent_df = df[df["test_id"].isin(recent_tests)]
        previous_df = df[df["test_id"].isin(previous_tests)]

        recent_mean = recent_df["reaction_time_adjusted"].mean()
        previous_mean = previous_df["reaction_time_adjusted"].mean()

        improvement = ((previous_mean - recent_mean) / previous_mean) * 100

        # ------------------- Tendência semântica -------------------
        if improvement > stable_threshold:
            trend = "improving"
        elif improvement < -stable_threshold:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "window_size": int(window_size),

            "previous_tests": [int(t) for t in previous_tests],
            "recent_tests": [int(t) for t in recent_tests],

            "previous_adj_mean": round(float(previous_mean), 1),
            "recent_adj_mean": round(float(recent_mean), 1),

            "improvement_percent": round(float(improvement), 1),
            "trend": trend
        }




    def remove_outliers_global(self, df, column="reaction_time", sensor_column="stimulus_id", k=1.5):
        def filter_sensor(sensor_df):
            sensor_df = sensor_df.copy()
            q1 = sensor_df[column].quantile(0.25)
            q3 = sensor_df[column].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - k * iqr
            upper = q3 + k * iqr

            return sensor_df[(sensor_df[column] >= lower) & (sensor_df[column] <= upper)]
        
        # Seleciona explicitamente todas as colunas (evita aviso futuro)
        df_clean = df.groupby(sensor_column, group_keys=False).apply(lambda x: filter_sensor(x), include_groups=False)

        return df_clean

   
    def get_last_sessions_stats(self, df_final, sessions_num):
        """
        Retorna estatísticas das últimas sessões do atleta, incluindo média ajustada,
        mediana, desvio padrão e percentual de melhoria em relação à sessão anterior.
        """
        if df_final.empty:
            return pd.DataFrame()  # retorna vazio se não houver dados

        # Identifica últimas 10 sessões
        last_sessions = df_final["test_id"].drop_duplicates().sort_values(ascending=False).head(sessions_num)
        df_last10 = df_final[df_final["test_id"].isin(last_sessions)]

        # Estatísticas por sessão
        session_stats = df_last10.groupby("test_id").agg({
            "reaction_time_adjusted": ["mean", "median", "std"]
        }).reset_index()

        # Renomeia colunas
        session_stats.columns = ["session_id", "mean_rt", "median_rt", "std_rt"]

        # Ordena do mais antigo para o mais recente
        session_stats = session_stats.sort_values("session_id").reset_index(drop=True)

        # Calcula melhoria percentual em relação à sessão anterior
        session_stats["prev_mean_rt"] = session_stats["mean_rt"].shift(1)
        session_stats["improvement_percent"] = (
            (session_stats["prev_mean_rt"] - session_stats["mean_rt"]) / session_stats["prev_mean_rt"] * 100
        )

        return session_stats