import os


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://mathsys:mathsys@localhost:5432/mathsys",
    )
    seed_on_start: bool = os.getenv("SEED_ON_START", "true").lower() == "true"


settings = Settings()
