from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


if os.getenv("PYTEST_RUNNING") == "1":
    load_dotenv(".env.test")
else:
    load_dotenv()


class Config(BaseSettings):
    app_name: str = "MyProjectFastApiTickts"
    debug: bool = False

    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore"
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


config = Config()
