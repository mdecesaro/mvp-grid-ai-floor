import sqlite3

def create_tables():
    import sqlite3

    conn = sqlite3.connect('../plataform.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            device_id TEXT,
            platform_version TEXT,
            timestamp TEXT NOT NULL,
            stimuli_count INTEGER,
            delay_type TEXT,
            delay_min_ms INTEGER,
            delay_max_ms INTEGER,
            execution_rounds INTEGER,
            timeout_ms INTEGER,
            repeat_if_wrong INTEGER,
            total_attempts INTEGER,
            hits INTEGER,
            errors INTEGER,
            avg_reaction_time REAL,
            duration_ms REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            round_num INTEGER NOT NULL,
            stimulus_id INTEGER NOT NULL,
            stimulus_position TEXT,
            stimulus_type TEXT,
            correct_color TEXT,
            reaction_time REAL,
            stimulus_start REAL,
            stimulus_end REAL,
            delay_ms INTEGER,
            elapsed_since_start REAL,
            error INTEGER,
            foot_used TEXT,
            wrong_stimulus_id TEXT,
            distractor_type TEXT,
            distractor_id_color TEXT, -- podemos armazenar JSON
            FOREIGN KEY (test_id) REFERENCES evaluation_tests (id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_eval_test_results_test_id
                    ON evaluation_test_results (test_id)
                """)

    conn.commit()
    conn.close()

# Criar as tabelas no banco
create_tables()
