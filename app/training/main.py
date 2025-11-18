from app.config.config import DATABASE_PATH
from app.context import AppContext
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold, GridSearchCV, cross_val_predict
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import matplotlib.pyplot as plt

def generalize_sector(sector):
    sector = sector.lower()
    if "frontal" in sector:
        return "frontal"
    elif "lateral" in sector:
        return "lateral"
    elif "diagonal" in sector:
        return "diagonal"
    elif "back" in sector:
        return "back"
    else:
        return "other"

def remove_outliers_iqr(df, col="reaction_time", group_cols=None, k=1.5):
    if group_cols is None:
        group_cols = []

    results = []
    for _, sub_df in df.groupby(group_cols):
        q1 = sub_df[col].quantile(0.25)
        q3 = sub_df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        results.append(sub_df[(sub_df[col] >= lower) & (sub_df[col] <= upper)])
    return pd.concat(results).reset_index(drop=True)

def run_training_with_gridsearch(X, y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Modelos e parâmetros
    models = {
        "Linear Regression": {
            "model": LinearRegression(),
            "params": {}
        },
        "Ridge Regression": {
            "model": Ridge(),
            "params": {"alpha": [0.1, 1.0, 10.0, 50.0]}
        },
        "Lasso Regression": {
            "model": Lasso(max_iter=5000),
            "params": {"alpha": [0.001, 0.01, 0.1, 1.0, 10.0]}
        },
        "Random Forest": {
            "model": RandomForestRegressor(random_state=42),
            "params": {
                "n_estimators": [200, 500],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5]
            }
        },
        "Gradient Boosting": {
            "model": GradientBoostingRegressor(random_state=42),
            "params": {
                "n_estimators": [200, 500],
                "learning_rate": [0.05, 0.1],
                "max_depth": [3, 5]
            }
        }
    }
    """,
    "AdaBoost": {
        "model": AdaBoostRegressor(
            estimator=DecisionTreeRegressor(random_state=42),
            random_state=42
        ),
        "params": {
            "n_estimators": [100, 200, 500],
            "learning_rate": [0.01, 0.05, 0.1, 0.5],
            "estimator__max_depth": [1, 3, 5]
        }
    }
    """


    for name, cfg in models.items():
        print(f"\n🔍 Rodando GridSearch para {name}...")

        # Pipeline: scaler + modelo
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('model', cfg["model"])
        ])

        # Ajusta parâmetros para usar no pipeline
        param_grid = {f"model__{key}": value for key, value in cfg["params"].items()}

        grid = GridSearchCV(
            pipe,
            param_grid,
            cv=kf,
            scoring="neg_mean_absolute_error",
            n_jobs=-1
        )
        grid.fit(X, y)

        best_model = grid.best_estimator_
        print(f"✅ Melhor parâmetros: {grid.best_params_}")

        # Avaliação via cross_val_predict
        y_pred_log = cross_val_predict(best_model, X, y, cv=kf)

        # Desfaz log para métricas na escala original
        y_pred = np.expm1(y_pred_log)
        y_true = np.expm1(y)

        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        print(f"{name} - R²: {r2:.3f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")

    # Importância das features para modelos que suportam
    if hasattr(best_model.named_steps['model'], 'feature_importances_'):
        importances = best_model.named_steps['model'].feature_importances_
        feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': importances}).sort_values(by='importance', ascending=False)
        print("Top Features:\n", feature_importance_df.head(10))

        # Plot
        plt.figure(figsize=(10,6))
        plt.barh(feature_importance_df['feature'], feature_importance_df['importance'])
        plt.gca().invert_yaxis()
        plt.title(f"Feature Importances - {name}")
        plt.show()

def run_training_with_models():
    context = AppContext(None, DATABASE_PATH)
    evaluation_dao = context.evaluation_dao
    dataset = evaluation_dao.select_data_for_training()
    df = pd.DataFrame(dataset)

    df = df.sort_values(by='result_id')

    # Sensor anterior
    df['prev_stimulus_id'] = df.groupby('test_id')['stimulus_id'].shift(1)
    df['prev_sensor_x'] = df.groupby('test_id')['x_c'].shift(1)
    df['prev_sensor_y'] = df.groupby('test_id')['y_c'].shift(1)

    # Dificuldade entre movimentos
    def calculate_difficulty(row):
        if pd.isna(row['prev_sensor_x']) or pd.isna(row['prev_sensor_y']):
            return 0
        dx = row['x_c'] - row['prev_sensor_x']
        dy = row['y_c'] - row['prev_sensor_y']
        return np.sqrt(dx**2 + dy**2)

    df['difficulty_transition'] = df.apply(calculate_difficulty, axis=1)

    # Setores
    df["sector_general"] = df["sector"].apply(generalize_sector)
    one_hot_cols = ["sector_general"]
    if "foot_used" in df.columns:
        one_hot_cols.append("foot_used")
    df = pd.get_dummies(df, columns=one_hot_cols, drop_first=True)

    # Remove outliers
    df_clean = remove_outliers_iqr(df, col="reaction_time", group_cols=["stimulus_id"], k=1.5)

    # Ângulo
    df_clean['angle_sin'] = np.sin(np.radians(df_clean['angle_norm']))
    df_clean['angle_cos'] = np.cos(np.radians(df_clean['angle_norm']))

    # Interações com distância
    df_clean['dist_x_sin'] = df_clean['dist_center_cm'] * df_clean['angle_sin']
    df_clean['dist_x_cos'] = df_clean['dist_center_cm'] * df_clean['angle_cos']

    # Features derivadas adicionais
    df_clean['dx'] = df_clean['x_c'] - df_clean['prev_sensor_x'].fillna(df_clean['x_c'])
    df_clean['dy'] = df_clean['y_c'] - df_clean['prev_sensor_y'].fillna(df_clean['y_c'])
    df_clean['angle_between_moves'] = np.arctan2(df_clean['dy'], df_clean['dx'])
    df_clean['difficulty_per_dist'] = df_clean['difficulty_transition'] / (df_clean['dist_center_cm'] + 1e-6)
    df_clean['difficulty_per_angle'] = df_clean['difficulty_transition'] / (df_clean['angle_norm'] + 1e-6)
    df_clean['dist_times_difficulty'] = df_clean['dist_center_cm'] * df_clean['difficulty_transition']
    df_clean['dist_times_angle'] = df_clean['dist_center_cm'] * df_clean['angle_norm']
    df_clean['difficulty_times_angle'] = df_clean['difficulty_transition'] * df_clean['angle_norm']
    df_clean['estimated_speed'] = df_clean['difficulty_transition'] / (df_clean['reaction_time'] + 1e-6)

    # Target transformado
    df_clean['reaction_time_log'] = np.log1p(df_clean['reaction_time'])
    y = df_clean['reaction_time_log']

    # Lista de features
    features = [
        'dist_center_cm', 'angle_sin', 'angle_cos', 'dist_x_sin', 'dist_x_cos', 'difficulty_transition',
        'dx', 'dy', 'angle_between_moves', 'difficulty_per_dist', 'difficulty_per_angle',
        'dist_times_difficulty', 'dist_times_angle', 'difficulty_times_angle', 'estimated_speed'
    ]

    # Adiciona colunas de setores e pé
    sector_cols = [col for col in df_clean.columns if col.startswith("sector_general_")]
    foot_cols = [col for col in df_clean.columns if col.startswith("foot_used_")]
    features += sector_cols + foot_cols

    # Cria matriz de features
    X = df_clean[features]

    run_training_with_gridsearch(X, y)

if __name__ == "__main__":
    run_training_with_models()
