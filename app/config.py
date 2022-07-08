from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = ...
    logging_config: str = "./logging.toml"

    class Config(object):
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()