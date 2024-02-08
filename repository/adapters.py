from typing import Any, List

from arango import ArangoClient
from psycopg2.extensions import connection, cursor

from repository.abstract import AbstractAdapter
from utils.utils import get_test_db


class PSqlAdapter(AbstractAdapter):

    def __init__(self, conn: connection):
        self.conn = conn
        self.cursor: cursor = conn.cursor()

    def execute(self, query: str, format_vars: List[Any] = ()) -> None:
        self.cursor.execute(query=query, vars=format_vars)

    def get(self, query: str, format_vars: List[str] = ()) -> list[Any]:
        self.execute(query=query, format_vars=format_vars)
        return self.cursor.fetchall()

    def create(self, query: str, format_vars: List[Any] = ()) -> None:
        self.execute(query=query, format_vars=format_vars)

    def add(self, query: str, format_vars: List[str] = ()) -> None:
        self.execute(query=query, format_vars=format_vars)


class ArangoAdapter(AbstractAdapter):
    def __init__(self, client: ArangoClient):
        self.client = client
        self.db = get_test_db(self.client)
        self.aql = self.db.aql

    def __enter__(self) -> 'ArangoAdapter':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def execute(self, query: Any, bind_vars=None) -> Any:
        if bind_vars is None:
            bind_vars = {}
        return self.aql.execute(query, bind_vars=bind_vars)
