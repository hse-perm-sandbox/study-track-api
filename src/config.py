from pydantic_settings import BaseSettings, SettingsConfigDict

CONN_STR_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    ECHO_DB_QUERIES: bool = True
    """Если True, то SQLAlchemy будет выводить все SQL-запросы в лог. Полезно для отладки."""

    @property
    def DATABASE_URL(self) -> str:
        return CONN_STR_TEMPLATE.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            dbname=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()