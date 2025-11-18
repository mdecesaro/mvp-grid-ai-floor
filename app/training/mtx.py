from app.config.config import DATABASE_PATH
from app.context import AppContext
import pandas as pd
import numpy as np

# --- Inicializa contexto e DAO ---
context = AppContext(None, DATABASE_PATH)
evaluation_dao = context.evaluation_dao

# --- Carrega dados reais ---
dataset = evaluation_dao.select_data_for_training()
df = pd.DataFrame(dataset)

# Ordenar pela sequência real
df = df.sort_values(by='result_id')
df = df[['test_id', 'stimulus_id', 'dist_center_cm', 'x_c', 'y_c']]

# Sensor anterior dentro de cada teste
df['prev_stimulus_id'] = df.groupby('test_id')['stimulus_id'].shift(1)
df['prev_sensor_x'] = df.groupby('test_id')['x_c'].shift(1)
df['prev_sensor_y'] = df.groupby('test_id')['y_c'].shift(1)

# Função para calcular dificuldade (distância euclidiana)
def calculate_difficulty(row):
    if pd.isna(row['prev_sensor_x']) or pd.isna(row['prev_sensor_y']):
        return 0  # primeiro movimento do teste
    dx = row['x_c'] - row['prev_sensor_x']
    dy = row['y_c'] - row['prev_sensor_y']
    return np.sqrt(dx**2 + dy**2)

# Aplicar a função
df['difficulty_transition'] = df.apply(calculate_difficulty, axis=1)


# Estatísticas da dificuldade
print("\n=== Estatísticas da dificuldade de transição ===")
print(df['difficulty_transition'].describe())