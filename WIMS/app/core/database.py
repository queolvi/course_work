import pyodbc
from app.core.config import Config


class Database:
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self) -> pyodbc.Connection:
        if self._connection is None:
            try:
                self._connection = pyodbc.connect(Config.get_connection_string())
                print(f"Success connect on db")
            except pyodbc.Error as e:
                print(f"Error connection, {e}")
                raise
        return self._connection
    
    def get_cursor(self) -> pyodbc.Cursor:
        conn = self.connect()
        return conn.cursor()
    
    def commit(self):
        if self._connection:
            self._connection.commit()
    
    def rollback(self):
        if self._connection:
            self._connection.rollback()
    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    
    def execute(self, query: str, params: tuple = ()) -> pyodbc.Cursor:
        cursor = self.get_cursor()
        cursor.execute(query, params)
        return cursor

db = Database()