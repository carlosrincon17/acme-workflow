from models.schemas import AccountCreate, Account, AccountValid, Condition

from repositories.account import AccountRepository
from repositories.step_result import StepResultRepository


class ConditionController:
    @classmethod
    def execute_condition(cls, condition: Condition, workflow_execution_id: str):
        filters = {
            "workflow_execution_id": workflow_execution_id,
            "step_id": condition.from_id,
        }
        validation_key = "result.{}".format(condition.field_id)
        if condition.operator == "eq":
            filters[validation_key] = condition.value
        else:
            filters[validation_key] = {
                "${}".format(condition.operator): condition.value
            }
        result_step = StepResultRepository.get_step_result(filters=filters)
        return result_step is not None
