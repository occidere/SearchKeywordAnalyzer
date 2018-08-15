from pymongo import MongoClient
import json


class SchKwdAnz:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.set_connection()

    def set_connection(self):
        path = "../resources/db.json"  # 특정 경로 가져오도록 수정해야 됨
        with open(path, 'r') as f:
            conf = json.load(f)['mongodb']
            url = conf['url']
            user = conf['user']
            pwd = conf['pwd']
            db_name = conf['db_name']
        self.client = MongoClient(url, username=user, password=pwd,
                                  authSource=db_name, authMechanism='SCRAM-SHA-256')
        self.db = self.client.schKwdAnz
        self.collection = self.db.nvSchKwd

    def insert_one(self, data):
        (k, v), = data.items()
        data = {"_id": k, "data": v}
        _id = self.collection.insert_one(data)
        return _id
