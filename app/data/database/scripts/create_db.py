import sqlite3

conn = sqlite3.connect('plataform.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY,
    col INTEGER,
    row INTEGER,
    sector TEXT,
    dist_center INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    country TEXT NOT NULL,    
    birth TEXT NOT NULL,
    dominant_foot TEXT NOT NULL,
    position TEXT NOT NULL,           
    profile BLOB NOT NULL,        
    timestamp TEXT DEFAULT (datetime('now'))   
)
""")

conn.commit()
conn.close()
print("Banco criado e tabelas prontas!")