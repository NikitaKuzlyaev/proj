from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    HASHING_ALGORITHM_LAYER_1 = 'bcrypt'
    HASHING_ALGORITHM_LAYER_2 = 'bcrypt'
    HASHING_SALT = 'ololo'

settings = Settings()