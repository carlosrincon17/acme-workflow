from datetime import datetime

from models.schemas import StepResult
from repositories.step_result import StepResultRepository


class StepResultController:
    @classmethod
    def create_step_result(
        cls, step_id: str, workflow_execution_id: str, result: dict
    ) -> StepResult:
        create_step_result = StepResult(
            step_id=step_id,
            workflow_execution_id=workflow_execution_id,
            result=result,
            create_date=datetime.utcnow(),
        )
        return StepResultRepository.create(step_result=create_step_result)
