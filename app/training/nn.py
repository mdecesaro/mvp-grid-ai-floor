from app.config.config import DATABASE_PATH
from app.context import AppContext
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

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

def run_nn_training(X, y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Padronização das features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    mlp = MLPRegressor(
        max_iter=5000,
        learning_rate_init=0.001,
        early_stopping=True,
        n_iter_no_change=50,
        random_state=42
    )
    param_grid = {
        'hidden_layer_sizes': [(32,), (64,), (32, 16)],
        'activation': ['relu', 'tanh'],
        'alpha': [0.0001, 0.001]
    }

    grid = GridSearchCV(mlp, param_grid, cv=kf, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid.fit(X_scaled, y)

    best_model = grid.best_estimator_
    print(f"✅ Melhor parâmetros: {grid.best_params_}")

    # Avaliação real via cross_val_score
    r2_scores = cross_val_score(best_model, X_scaled, y, cv=kf, scoring='r2')
    mae_scores = cross_val_score(best_model, X_scaled, y, cv=kf, scoring='neg_mean_absolute_error')
    rmse_scores = cross_val_score(best_model, X_scaled, y, cv=kf, scoring='neg_root_mean_squared_error')

    print(f"MLPRegressor - R²: {r2_scores.mean():.3f} ± {r2_scores.std():.3f}, "
          f"MAE: {-mae_scores.mean():.2f}, RMSE: {-rmse_scores.mean():.2f}")

def run_training_with_nn():
    # Inicializa contexto e DAO
    context = AppContext(None, DATABASE_PATH)
    evaluation_dao = context.evaluation_dao
    
    # Seleciona dados
    dataset = evaluation_dao.select_data_for_training()
    df = pd.DataFrame(dataset)
    df = df.sort_values(by='result_id')

    # Sensor anterior
    df['prev_stimulus_id'] = df.groupby('test_id')['stimulus_id'].shift(1)
    df['prev_sensor_x'] = df.groupby('test_id')['x_c'].shift(1)
    df['prev_sensor_y'] = df.groupby('test_id')['y_c'].shift(1)

    def calculate_difficulty(row):
        if pd.isna(row['prev_sensor_x']) or pd.isna(row['prev_sensor_y']):
            return 0
        dx = row['x_c'] - row['prev_sensor_x']
        dy = row['y_c'] - row['prev_sensor_y']
        return np.sqrt(dx**2 + dy**2)

    df['difficulty_transition'] = df.apply(calculate_difficulty, axis=1)

    # Cria coluna com setor agregado
    df["sector_general"] = df["sector"].apply(generalize_sector)

    # One-hot encoding seguro para setor e foot_used
    one_hot_cols = ["sector_general"]
    if "foot_used" in df.columns:
        one_hot_cols.append("foot_used")
    df = pd.get_dummies(df, columns=one_hot_cols, drop_first=True)
    
    # Filtra outliers extremos
    df_clean = remove_outliers_iqr(df, col="reaction_time", group_cols=["stimulus_id"], k=1.5)

    # Transformar ângulo em seno e cosseno
    df_clean['angle_sin'] = np.sin(np.radians(df_clean['angle_norm']))
    df_clean['angle_cos'] = np.cos(np.radians(df_clean['angle_norm']))

    # Criar interações com distância
    df_clean['dist_x_sin'] = df_clean['dist_center_cm'] * df_clean['angle_sin']
    df_clean['dist_x_cos'] = df_clean['dist_center_cm'] * df_clean['angle_cos']
    
    # Seleciona features
    features = ['dist_center_cm', 'angle_sin', 'angle_cos', 'dist_x_sin', 'dist_x_cos', 'difficulty_transition']
   
    sector_cols = [col for col in df_clean.columns if col.startswith("sector_general_")]
    foot_cols = [col for col in df_clean.columns if col.startswith("foot_used_")]
    features += sector_cols + foot_cols

    X = df_clean[features]
    y = df_clean["reaction_time"]

    run_nn_training(X, y)

if __name__ == "__main__":
    run_training_with_nn()
