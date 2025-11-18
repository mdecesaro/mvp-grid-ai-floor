import math
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

class AthleteStats:
    def __init__(self, context, athlete_id: int,
                 hex_width=17.0, hex_height=15.0, gap=2.0,
                 normalize_method=None, normalize_reference='mean'):
        
        self.context = context
        self.athlete_id = athlete_id
        self.hex_width = hex_width
        self.hex_height = hex_height
        self.gap = gap
        self.normalize_method = normalize_method
        self.normalize_reference = normalize_reference

        self.evaluation_dao = context.evaluation_dao

        self.retrive_data()
        self.create_rl_multipla()
        #self._normalize_reaction_times()
        #self.create_reg()

    """
    def create_reg(self):
        df_unique = self.df[["stimulus_id", "dist_center_real", "angle_norm"]].drop_duplicates()
        df_min_time = self.df.groupby("stimulus_id")["reaction_time"].min().reset_index()
        df_final = df_unique.merge(df_min_time, on="stimulus_id", how="left")
        df_final = df_final.sort_values(by="dist_center_real", ascending=True).reset_index(drop=True)
        
        print(df_final)
    """

    def retrive_data(self):
        """Carrega dataset do DAO e transforma em DataFrame"""
        self.dataset = self.evaluation_dao.select_tests_with_results_by_athlete(self.athlete_id)
        self.df = pd.DataFrame(self.dataset)

        # imprime todas as colunas disponíveis
        #print("Colunas disponíveis:", self.df.columns.tolist())

    def create_rl_multipla(self):
        # Features (X) and target (y)
        X = self.df[["dist_center_cm", "angle_norm"]]
        y = self.df["reaction_time"]

        # Model
        lin_reg = LinearRegression()
        lin_reg.fit(X, y)

        # Predict
        self.df["predicted_time"] = lin_reg.predict(X)

        # Resíduo: quanto o atleta foi mais rápido (+) ou mais lento (-) que o previsto
        self.df["residual"] = self.df["reaction_time"] - self.df["predicted_time"]

        # Eficiência: razão entre previsto e real (>1 = mais rápido que esperado, <1 = mais lento)
        self.df["efficiency"] = self.df["predicted_time"] / self.df["reaction_time"]

        # Média por sensor
        sensor_stats = self.df.groupby("stimulus_id")[["residual", "efficiency"]].mean()

        # Média por ângulo (setores)
        angle_stats = self.df.groupby("angle_norm")[["residual", "efficiency"]].mean()

        # Média por distância
        dist_stats = self.df.groupby("dist_center_cm")[["residual", "efficiency"]].mean()

        print(
            self.df[[
                "stimulus_id",
                "dist_center_cm",
                "angle_norm",
                "reaction_time",
                "predicted_time",
                "residual",
                "efficiency"
            ]].head()
)

    

   
