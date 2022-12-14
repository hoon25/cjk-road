from pymongo import MongoClient

client = MongoClient('54.180.145.4', 27017,
                     username='test',
                     password='test',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-1'
                     )


def get_db():
    db = client.cjk
    return db


def get_conn_with_collections(collection_name):
    db = client.cjk
    collections = db[collection_name]
    return collections


def save_data(collection_name, data):
    collections = get_conn_with_collections(collection_name)
    collections.insert_many(data)
