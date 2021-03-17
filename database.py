from pymongo import MongoClient
from settings import mongo_settings as settings
playvox_mongo_client = MongoClient(settings.uri).get_database(settings.database)
