import sqlite3
import json
import math

def calc_hex_radius():
    hex_width=17.0
    hex_height=15.0
    gap=0
    
    width_eff = hex_width + gap
    height_eff = hex_height + gap
    R_from_width = width_eff / math.sqrt(3) 
    R_from_height = height_eff / 2

    return (R_from_width + R_from_height) / 2.0

def hex_to_cm(q, r):
    R = calc_hex_radius()
    x = 1.5 * R * q
    y = math.sqrt(3) * R * (r + q/2)
    return x, y

def angle_0_180_lateral(q, r, q_center=0, r_center=0):
    x0, y0 = hex_to_cm(q_center, r_center)
    x, y = hex_to_cm(q, r)
    
    dx = x - x0
    dy = y - y0
    if dy == 0 and dx == 0:
        return 0
    if dx >= 0:
        angle = math.degrees(math.atan2(dx, -dy))
    else:
        angle = math.degrees(math.atan2(-dx, -dy))
    
    if angle < 0:
        angle += 360
    if angle > 180:
        angle = 180
    
    return round(angle, 1)

def xy_to_distance(x, y):
    return (x **2 + y**2)**0.5

def classify_movement(angle):
    if 0 <= angle <= 60:
        return "direct_extension"
    elif 60 < angle <= 120:
        return "transition"
    elif 120 < angle <= 180:
        return "pivot_rotation"
    else:
        return "undefined"

def normalize_angle(angle, step=5):
    return round(angle / step) * step

# JSON completo (copie exatamente o conteúdo que você enviou acima)
with open("sensors.json", "r", encoding="utf-8") as file:
    sensors = json.load(file)

# Conecta (ou cria) o banco de dados SQLite
conn = sqlite3.connect("../plataform.db")
cursor = conn.cursor()

# Garante que a tabela existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor INTEGER,
    layout TEXT,
    sector TEXT,
    expected_foot TEXT,
    dist_center INTEGER,
    dist_center_cm REAL,      
    q INTEGER,
    r INTEGER,
    x_c integer,
    y_c integer,                       
    angle REAL,
    angle_norm REAL,
    range_type TEXT,                    
    neighbors TEXT
)
""")

cursor.execute("""
CREATE TABLE movement_ranges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    range_type TEXT UNIQUE,
    angle_min REAL,
    angle_max REAL,
    description TEXT
)
""")

cursor.execute("""
INSERT INTO movement_ranges (range_type, angle_min, angle_max, description) VALUES
('direct_extension', 0, 60, 'The athlete reaches only with leg/hip extension, no body rotation'),
('transition', 60, 120, 'The athlete may choose extension or partial pivot rotation'),
('pivot_rotation', 120, 180, 'Requires pivot or body rotation to reach')
""")

# Insere os sensores
for sensor in sensors:
    sen = sensor["sensor"]
    layout = sensor["layout"]
    sector = sensor["position"]
    expected_foot = sensor["expected_foot"]
    depth = sensor["depth"]
    q = sensor["q"]
    r = sensor["r"]
    x, y = hex_to_cm(q, r)
    dist_center_cm = xy_to_distance(x, y) 
    angle = angle_0_180_lateral(q, r) 
    angle_norm = normalize_angle(angle, step=5)
    range_type = classify_movement(angle)
    neighbors = json.dumps(sensor["neighbors"]) 

    cursor.execute("""
        INSERT INTO sensors (sensor, layout, sector, expected_foot, dist_center, dist_center_cm, q, r, x_c, y_c, angle, angle_norm, range_type, neighbors)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (sen, layout, sector, expected_foot, depth, dist_center_cm, q, r, x, y, angle, angle_norm, range_type, neighbors))

# Finaliza
conn.commit()
conn.close()

print("Sensores inseridos com sucesso!")
