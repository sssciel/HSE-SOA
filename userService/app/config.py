from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).absolute().parent.joinpath(".env")
    )


config = Config()


def get_db_url():
    return (
        f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@"
        f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )


def get_auth_data():
    return {"secret_key": config.SECRET_KEY, "algorithm": config.ALGORITHM}
