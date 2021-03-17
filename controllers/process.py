from typing import List

from bson import ObjectId

from controllers.account import AccountController
from controllers.condition import ConditionController
from controllers.step_result import StepResultController
from exceptions.work_flow_exception import StepNotFoundException
from models.schemas import Step, Transition, Trigger
from repositories.step_repository import StepRepository
from repositories.step_result import StepResultRepository
from util.decorators import log_transition


class ProcessController:

    def __init__(self, trigger: Trigger, workflow_execution_id: str):
        self.workflow_execution_id = workflow_execution_id
        StepResultController.create_step_result(
            step_id=trigger.id,
            workflow_execution_id=workflow_execution_id,
            result=trigger.params
        )

    def process_step(self, step: Step):
        action_data = {}
        for parameter_name in step.params:
            action_data[parameter_name] = self.__get_params_values(
                step=step,
                parameter_name=parameter_name
            )
        action_result = AccountController().handle_action(step.action, **action_data)
        StepResultController.create_step_result(
            step_id=step.id,
            workflow_execution_id=self.workflow_execution_id,
            result=action_result
        )
        self.process_transitions(transitions=step.transitions)

    def process_transitions(self, transitions: List[Transition]):
        for transition in transitions:
            if self.__process_transition(transition):
                next_step_filter = {'id': transition.target,
                                    'workflow_execution_id': ObjectId(self.workflow_execution_id)}
                next_step = StepRepository.get_step(filters=next_step_filter)
                if not next_step:
                    raise StepNotFoundException(step_name=transition.target)
                self.process_step(step=next_step)

    @log_transition
    def __process_transition(self, transition: Transition) -> bool:
        if transition.condition:
            for condition in transition.condition:
                condition_result = ConditionController.execute_condition(
                    condition=condition,
                    workflow_execution_id=self.workflow_execution_id
                )
                if not condition_result:
                    return condition_result
        return True

    def __get_params_values(self, step, parameter_name):
        params_config = step.params[parameter_name]
        if params_config.get('value'):
            return params_config.get('value')
        last_value = StepResultRepository.get_last_step_result(
            step=params_config.get('from_id'),
            workflow_execution_id=self.workflow_execution_id
        )
        if last_value:
            return last_value.get(params_config.get('param_id'))
        return None

