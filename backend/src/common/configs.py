import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    database: str
    user: str
    password: str
    port: str

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        load_dotenv()
        if not os.getenv("DB_NAME") or not os.getenv("DB_USER"):
            raise ValueError("Missing critical database environment variables.")

        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=os.getenv("DB_PORT", "5432"),
        )
