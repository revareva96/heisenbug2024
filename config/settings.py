from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5432
    database: str = 'admin'
    schema: str = 'public'
    user: str = 'admin'
    password: str = 'test123'


class ArangoDBSettings(BaseSettings):
    ...
