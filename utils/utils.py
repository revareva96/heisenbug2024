from arango import ArangoClient
from arango.database import Database

from config.settings import get_arango_settings

arango_settings = get_arango_settings()
username = arango_settings.username
password = arango_settings.password


def get_test_db(client: ArangoClient) -> Database:
    system_db = client.db('_system', username=username, password=password)
    if not system_db.has_database('test'):
        system_db.create_database('test')
    return client.db('test', username=username, password=password)
