import pymongo
from settings import mongo_settings as settings

database_uri = settings.uri.format(settings.username, settings.password)
playvox_mongo_client = pymongo.MongoClient(database_uri).get_database(settings.database)
