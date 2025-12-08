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
    
    def compare_last_session(self, df):
        """Compara os últimos dois testes do atleta."""
        last_test = df["test_id"].max()
        prev_test = df["test_id"].unique()
        prev_test = [t for t in prev_test if t != last_test]

        if len(prev_test) == 0:
            return None

        prev_test = max(prev_test)

        last_df = df[df["test_id"] == last_test]
        prev_df = df[df["test_id"] == prev_test]

        last_mean = last_df["reaction_time_adjusted"].mean()
        prev_mean = prev_df["reaction_time_adjusted"].mean()

        improvement = ((prev_mean - last_mean) / prev_mean) * 100

        return {
            "previous_test_id": prev_test,
            "last_test_id": last_test,
            "prev_adj_mean": prev_mean,
            "last_adj_mean": last_mean,
            "improvement_percent": improvement
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
        df_clean = df.groupby(sensor_column, group_keys=False).apply(lambda x: filter_sensor(x))

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