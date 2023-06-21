from pydantic import BaseSettings, SecretStr


class Config(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_config() -> Config:
    return Config()
