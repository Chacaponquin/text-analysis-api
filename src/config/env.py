from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE: str = 'messages'


ENVS = Settings()

