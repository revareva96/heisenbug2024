from arango.client import ArangoClient
from arango.database import Database

from config.settings import get_arango_settings
from queries.arango_queries import check_data, create_dirs, create_edges, get_dirs
from repository.adapters import ArangoAdapter

arango_settings = get_arango_settings()
username = arango_settings.username
password = arango_settings.password


def get_test_db(client: ArangoClient) -> Database:
    system_db = client.db('_system', username=username, password=password)
    if not system_db.has_database('test'):
        system_db.create_database('test')
    return client.db('test', username=username, password=password)


def create_collections(adapter: ArangoAdapter) -> None:
    if not adapter.db.has_collection('Dirs'):
        adapter.db.create_collection('Dirs', key_generator='uuid')
    if not adapter.db.has_collection('Subdirs'):
        adapter.db.create_collection('Subdirs', edge=True, key_generator='uuid')


def fill_collections(adapter: ArangoAdapter) -> None:
    if list(adapter.execute(check_data)):
        return
    data = list(adapter.execute(create_dirs, bind_vars={
        'dirs': ['dir', 'dir_1', 'dir_1_1', 'dir_1_2', 'dir_2', 'dir_2_1', 'dir_2_2', 'dir_3', 'dir_3_1', 'dir_3_2']}))
    root = data[0]

    for level in range(3):
        level_one = data[1 + level * 3]['_id']
        level_two1, level_two2 = data[2 + level * 3]['_id'], data[3 + level * 3]['_id']
        adapter.execute(create_edges, bind_vars={'_from': root['_id'], '_to': level_one})
        adapter.execute(create_edges, bind_vars={'_from': level_one, '_to': level_two1})
        adapter.execute(create_edges, bind_vars={'_from': level_one, '_to': level_two2})


def get_arango_data(adapter: ArangoAdapter, name: str = 'dir') -> list:
    return list(adapter.aql.execute(get_dirs, bind_vars={'name': name}))
