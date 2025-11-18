import sqlite3

conn = sqlite3.connect('../plataform.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,  
    name TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
INSERT INTO categories (code, name, description) VALUES
('cognitive', 'Cognitive', 'Exercises that improve decision-making, memory, and attention.'),
('performance', 'Performance', 'Exercises focused on reaction time and execution speed.'),
('coordination', 'Coordination', 'Exercises that improve precision and motor control.'),
('conditioning', 'Conditioning', 'Exercises for endurance, intensity, and training volume.')
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    level INTEGER NOT NULL DEFAULT 1,
    objective TEXT NOT NULL,
    modality TEXT NOT NULL,
    parameters TEXT NOT NULL,
    board_size INTEGER NOT NULL,       
    active INTEGER DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

print("Tables created!")