from typing import Any, List

from psycopg2.extensions import cursor

from repository.abstract import AbstractAdapter


class PSqlAdapter(AbstractAdapter):

    def __init__(self, psql_cursor: cursor):
        self.cursor = psql_cursor

    def execute(self, query: str, format_vars: List[Any] = ()) -> None:
        self.cursor.execute(query=query, vars=format_vars)

    def get(self, query: str, format_vars: List[str] = ()) -> list[Any]:
        self.execute(query=query, format_vars=format_vars)
        return self.cursor.fetchall()

    def create(self, query: str, format_vars: List[Any] = ()) -> None:
        self.execute(query=query, format_vars=format_vars)

    def add(self, query: str, format_vars: List[str] = ()) -> None:
        self.execute(query=query, format_vars=format_vars)
