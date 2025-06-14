from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    KAFKA_BROKER: str
    CLICKHOUSE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).absolute().parent.parent.joinpath(".env")
    )


config = Config()


def get_kafka_broker() -> str:
    return config.KAFKA_BROKER


def get_clickhouse_url() -> str:
    return config.CLICKHOUSE_URL
