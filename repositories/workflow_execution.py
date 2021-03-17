from models.schemas import Trigger, WorkflowExecution
from repositories.base_repository import BaseRepository


class WorkFlowExecutionRepository(BaseRepository):

    __collection__ = "workflow_execution"

    @classmethod
    def create(cls, trigger: Trigger) -> WorkflowExecution:
        workflow_execution = WorkflowExecution(trigger=trigger)
        result = cls.get_collection().insert_one(workflow_execution.dict())
        return cls.get_workflow_execution({"_id": result.inserted_id})

    @classmethod
    def get_workflow_execution(cls, filters) -> WorkflowExecution:
        workflow_execution = cls.get_collection().find_one(filters)
        return WorkflowExecution(**workflow_execution) if workflow_execution else None
