from bson import ObjectId

from models.schemas import Step
from repositories.base_repository import BaseRepository


class StepRepository(BaseRepository):

    __collection__ = "steps"

    @classmethod
    def create(cls, step: Step) -> Step:
        result = cls.get_collection().insert_one(step.dict())
        return cls.get_step({"_id": ObjectId(result.inserted_id)})

    @classmethod
    def get_step(cls, filters) -> Step:
        step = cls.get_collection().find_one(filters)
        return Step(**step) if step else None
