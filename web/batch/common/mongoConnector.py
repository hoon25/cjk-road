from pymongo import MongoClient

def get_client():
    client = MongoClient('54.180.145.4', 27017,
                         username='test',
                         password='test',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-1'
                         )
    return client


def get_conn():
    client = get_client()
    db = client.cjk
    return db


def save_data(collection_name, data):
    client = get_client()
    db = client.cjk
    collections = db[collection_name]
    collections.insert_many(data)
    client.close()





