from pydantic_settings import BaseSettings, SettingsConfigDict

CONN_STR_TEMPLATE = "postgresql+asyncpg://{user}:@{host}:{port}/{dbname}"


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "postgres"
    ECHO_DB_QUERIES: bool = True
    """Если True, то SQLAlchemy будет выводить все SQL-запросы в лог. Полезно для отладки."""

    @property
    def DATABASE_URL(self) -> str:
        if self.POSTGRES_PASSWORD:
            return CONN_STR_TEMPLATE.format(
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                dbname=self.POSTGRES_DB,
            )
        
        return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
