from arango import ArangoClient

import psycopg2

from config.settings import get_arango_settings, get_postgesql_settings
from repository.adapters import PSqlAdapter, ArangoAdapter
from services.arango_services import create_collections, fill_collections, get_arango_data
from services.psql_services import create_tables, fill_tables, get_data_recursive

if __name__ == '__main__':
    psql_settings = get_postgesql_settings()
    arango_settings = get_arango_settings()

    with psycopg2.connect(**psql_settings.model_dump(exclude={'schema'})) as conn:
        psq_adapter = PSqlAdapter(conn)
        create_tables(psq_adapter)
        conn.commit()  # todo: create UnitOfWork
        fill_tables(psq_adapter)
        conn.commit()  # todo: create UnitOfWork
        result = get_data_recursive(psq_adapter, ['dir', '4'])
        print('result - ', result)

    with ArangoAdapter(ArangoClient(hosts=f'http://{arango_settings.host}:{arango_settings.port}')) as arango_adapter:
        create_collections(arango_adapter)
        fill_collections(arango_adapter)
        result = get_arango_data(arango_adapter, name='dir')
        print('result - ', result)
