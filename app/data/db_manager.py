import sqlite3
import threading

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._init(db_path)
        return cls._instance

    def _init(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __enter__(self):
        """Permite usar with DatabaseManager(db_path) as db:"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garante que commit/close aconteçam corretamente"""
        if exc_type is None:
            self.commit()
        else:
            self.conn.rollback()
        
    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            DatabaseManager._instance = None
