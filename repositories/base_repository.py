from pymongo.collection import Collection

from database import playvox_mongo_client


class BaseRepository:

    __collection__ = None

    @classmethod
    def get_collection(cls) -> Collection:
        collection: Collection = playvox_mongo_client.get_collection(cls.__collection__)
        return collection
