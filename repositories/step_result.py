import pymongo
from bson import ObjectId

from models.schemas import StepResult
from repositories.base_repository import BaseRepository


class StepResultRepository(BaseRepository):

    __collection__ = "step_results"

    @classmethod
    def create(cls, step_result: StepResult) -> StepResult:
        result = cls.get_collection().insert_one(step_result.dict())
        return cls.get_step_result({"_id": ObjectId(result.inserted_id)})

    @classmethod
    def get_step_result(cls, filters) -> StepResult:
        step_result = cls.get_collection().find_one(filters)
        return StepResult(**step_result) if step_result else None

    @classmethod
    def get_last_step_result(cls, step: str, workflow_execution_id: str) -> dict:
        filters = {"step_id": step, "workflow_execution_id": workflow_execution_id}
        step_result = cls.get_collection().find_one(
            filter=filters, sort=[("create_date", pymongo.DESCENDING)]
        )
        return StepResult(**step_result).result if step_result else None
