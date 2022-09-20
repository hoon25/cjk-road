from pymongo import MongoClient

client = MongoClient('13.209.42.162', 27017,
                     username='test',
                     password='test',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-1'
                     )


def get_conn_with_collections(collection_name):
    db = client.cjk
    collections = db[collection_name]
    return collections


def save_data(collection_name, data):
    collections = get_conn_with_collections(collection_name)
    collections.insert_many(data)




