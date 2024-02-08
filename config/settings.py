from pydantic_settings import BaseSettings
from functools import cache


class PostgresSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5432
    database: str = 'admin'
    schema: str = 'public'
    user: str = 'admin'
    password: str = 'test123'


class ArangoDBSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 8529
    username: str = 'root'
    password: str = 'test123'


@cache
def get_postgesql_settings() -> PostgresSettings:
    return PostgresSettings()


@cache
def get_arango_settings() -> ArangoDBSettings:
    return ArangoDBSettings()
