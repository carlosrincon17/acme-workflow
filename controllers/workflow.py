from controllers.process import ProcessController
from models.schemas import WorkflowSuccessResponse
from repositories.step_repository import StepRepository
from repositories.workflow_execution import WorkFlowExecutionRepository
from util.decorators import process_exception


class WorkFlowController:

    @staticmethod
    @process_exception
    def process_workflow(workflow) -> WorkflowSuccessResponse:
        workflow_execution = WorkFlowExecutionRepository.create(trigger=workflow.trigger)
        for step in workflow.steps:
            step.workflow_execution_id = workflow_execution.id
            StepRepository.create(step=step)
        process_controller = ProcessController(
            workflow_execution_id=str(workflow_execution.id),
            trigger=workflow.trigger
        )
        process_controller.process_transitions(workflow.trigger.transitions)
        workflow_result = WorkflowSuccessResponse(
            message="Workflow was processed successfully!"
        )
        return workflow_result
