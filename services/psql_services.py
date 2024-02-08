from typing import Any

from psycopg2.extensions import AsIs

from config.settings import get_postgesql_settings
from queries.psql_queries import create_dirs, create_edges, table_exist, get_recursive_data
from repository.adapters import PSqlAdapter

settings = get_postgesql_settings()
schema = settings.schema


def create_tables(psql_adapter: PSqlAdapter) -> None:
    table_dirs_exist = psql_adapter.get(table_exist, ['dirs'])
    if not table_dirs_exist:
        psql_adapter.create(create_dirs, [AsIs(f'{schema}.dirs')])

    table_edges_exist = psql_adapter.get(table_exist, ['edges_dirs'])
    if not table_edges_exist:
        psql_adapter.create(create_edges, [AsIs(f'{schema}.edges_dirs')])


def fill_tables(psql_adapter: PSqlAdapter) -> None:
    if psql_adapter.get(f'select * from {schema}.dirs limit 1;'):
        return
    query_dirs = f'insert into {schema}.dirs (name) values '
    query_edges = f'insert into {schema}.edges_dirs (head_id, tail_id) values '
    root_dir_name = "'dir'"
    _id = 1
    query_dirs += f'({root_dir_name})'
    base_dir_name = "dir"
    # add first level od dirs
    for level_one in range(1, 4):
        key = base_dir_name + f'_{level_one}'
        _id_one = _id + (level_one - 1) * 2 + level_one
        query_dirs += f", ('{key}')"
        query_edges += f"({_id}, {_id_one}), "
        # add first level od dirs
        for level_two in range(1, 3):
            key_2 = key + f'_{level_two}'
            _id_two = _id_one + level_two
            query_edges += f"({_id_one}, {_id_two}), "
            query_dirs += f", ('{key_2}')"
    psql_adapter.execute(query=query_dirs)
    psql_adapter.execute(query=query_edges[:-2])


def get_data_recursive(psql_adapter: PSqlAdapter, format_vars=None) -> list[Any]:
    if format_vars is None:
        format_vars = ['.root', '2']
    return psql_adapter.get(query=get_recursive_data, format_vars=format_vars)
