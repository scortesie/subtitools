import os
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId


USER = os.environ['MONGO_DBUSER']
PASSWORD = os.environ['MONGO_DBPASSWORD']
HOST = os.environ['MONGO_HOST']
PORT = os.environ['MONGO_PORT']
DB = os.environ['MONGO_DB']


class Subtitles(object):
    @staticmethod
    def get_mongo_client():
        return MongoClient(
            'mongodb://{user}:{password}@{host}:{port}/{db}'.format(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                db=DB))

    def __init__(self):
        self.client = Subtitles.get_mongo_client()

    def remove_documents_older_than(self, object_id, minutes=120):
        _id = ObjectId.from_datetime(
            object_id.generation_time - datetime.timedelta(minutes=minutes))
        self.client[DB].subtitles.remove(
            {'_id': {'$lte': _id}})

    def insert(self, subtitles):
        return self.client[DB].subtitles.insert_one(
            {'list': subtitles})

    def find_by_id(self, _id):
        return self.client[DB].subtitles.find_one({'_id': ObjectId(_id)})

    def remove_by_id(self, _id):
        self.client[DB].subtitles.remove({'_id': ObjectId(_id)})
