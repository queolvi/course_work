import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "Warehouse")
    DB_USER: str = os.getenv("DB_USER", "app_login")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "app_pswd")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    
    
    @classmethod
    def get_connection_string(cls) -> str:
        return (
            f"DRIVER={cls.DB_DRIVER};"
            f"SERVER={cls.DB_SERVER};"
            f"DATABASE={cls.DB_NAME};"
            f"UID={cls.DB_USER};"
            f"PWD={cls.DB_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )