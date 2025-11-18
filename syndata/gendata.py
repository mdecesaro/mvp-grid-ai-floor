import pandas as pd
import numpy as np
import random
from app.data.db_manager import DatabaseManager
from app.data.dao.evaluation_dao import EvaluationDAO

db = DatabaseManager("app/data/database/plataform.db")
eval_dao = EvaluationDAO(db)

# === Dados originais do treino ===
data = [
    # round, test_id, stimulus_id, stimulus_position, stimulus_type, correct_color, reaction_time, foot_used, error
    [1,1,10,"Frontal Left","color","green",692.19,"Left",0],
    [1,1,21,"Frontal Right","color","green",562.72,"Right",0],
    [1,1,14,"Frontal","color","green",831.62,"Either",0],
    [1,1,6,"Diagonal Left Up","color","green",664.62,"Left",0],
    [1,1,9,"Diagonal Left Down","color","green",664.54,"Left",0],
    [1,1,29,"Diagonal Right up","color","green",729.77,"Right",0],
    [1,1,17,"Back","color","green",694.07,"Either",0],
    [1,1,18,"Back","color","green",748.03,"Either",0],
    [1,1,1,"Diagonal Left Up","color","green",927.91,"Left",0],
    [1,1,15,"Frontal","color","green",600.74,"Either",0],
    [1,1,28,"Diagonal Right down","color","green",805.40,"Right",0],
    [1,1,19,"Back","color","green",1189.06,"Either",0],
    [1,1,26,"Lateral Right","color","green",375.67,"Right",1],
    [1,1,16,"Frontal","color","green",535.71,"Either",0],
    [1,1,3,"Lateral Left","color","green",748.18,"Left",0],
    [1,1,30,"Lateral Right","color","green",663.20,"Right",0],
    [1,1,20,"Frontal Right","color","green",828.63,"Right",0],
    [1,1,7,"Lateral left","color","green",753.61,"Left",0],
    [1,1,32,"Diagonal Right down","color","green",1272.82,"Right",0],
    [1,1,24,"Diagonal Right up","color","green",650.25,"Right",0],
    [1,1,22,"Back Right","color","green",918.54,"Right",0],
    [1,1,11,"Frontal Left","color","green",726.70,"Left",0],
    [1,1,31,"Lateral Right","color","green",699.46,"Right",0],
    [1,1,5,"Diagonal Left Up","color","green",864.04,"Left",0],
    [1,1,23,"Back Right","color","green",444.75,"Right",1],
    [1,1,8,"Diagonal left down","color","green",726.56,"Left",0],
    [1,1,25,"Diagonal Right up","color","green",513.26,"Right",0],
    [1,1,2,"Lateral Left","color","green",791.22,"Left",0],
    [1,1,27,"Diagonal Right down","color","green",503.44,"Right",0],
    [1,1,13,"Back Left","color","green",860.98,"Left",0],
    [1,1,4,"Diagonal Left Down","color","green",690.18,"Left",0],
    [1,1,12,"Back Left","color","green",608.11,"Left",0],
]

columns = ["round","test_id","stimulus_id","stimulus_position","stimulus_type","correct_color",
           "reaction_time","foot_used","error"]

df = pd.DataFrame(data, columns=columns)

# === Função para gerar dados sintéticos ===
def generate_synthetic_data(df, n_rounds=6):
    synthetic = []
    current_round = 2
    for r in range(n_rounds):
        for _, row in df.iterrows():
            # Pequenas variações nos tempos de reação ±15%
            rt = row["reaction_time"] * np.random.uniform(0.85, 1.15)
            # Mantém a proporção de erros
            error = row["error"] if random.random() > 0.1 else 1 - row["error"]
            synthetic.append([
                current_round,
                row["test_id"],
                row["stimulus_id"],
                row["stimulus_position"],
                row["stimulus_type"],
                row["correct_color"],
                round(rt,2),
                row["foot_used"],
                error
            ])
        current_round += 1
    return pd.DataFrame(synthetic, columns=columns)

# Gerar dados sintéticos
synthetic_df = generate_synthetic_data(df, n_rounds=5)

# Salvar para teste ou para carregar no MVP
synthetic_df.to_csv("synthetic_data.csv", index=False)

print("Dados sintéticos gerados:")
print(synthetic_df.head(10))
