import psycopg2

from config.settings import PostgresSettings
from repository.adapters import PSqlAdapter
from services.psql_services import create_tables, fill_tables, get_data_recursive

import warnings

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    psql_settings = PostgresSettings()
    db = psql_settings.database
    schema = psql_settings.schema

    with psycopg2.connect(**psql_settings.model_dump(exclude={'schema'})) as conn:
        cursor = conn.cursor()
        psq_adapter = PSqlAdapter(cursor)
        create_tables(psq_adapter)
        conn.commit()
        fill_tables(psq_adapter)
        conn.commit()
        result = get_data_recursive(psq_adapter, ['dir_3'])
        print('result - ', result)
