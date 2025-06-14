from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

LIST_ON_PAGE = 10


class Config(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    USER_SERVICE_URL: str
    POST_SERVICE_URL: str
    STATS_SERVICE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).absolute().parent.parent.joinpath(".env")
    )


config = Config()


def get_user_service_url():
    return config.USER_SERVICE_URL


def get_post_service_url():
    return config.POST_SERVICE_URL


def get_stat_service_url():
    return config.STATS_SERVICE_URL


def get_auth_data():
    return {"secret_key": config.SECRET_KEY, "algorithm": config.ALGORITHM}
