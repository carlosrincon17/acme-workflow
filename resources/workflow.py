from http import HTTPStatus
from json import JSONDecodeError

from fastapi import UploadFile, File, HTTPException
from fastapi_restful import Resource, set_responses

from controllers.workflow import WorkFlowController
from models.schemas import Account, WorkFlow, WorkflowSuccessResponse
import json


class WorkFlowApi(Resource):

    @set_responses(
        WorkflowSuccessResponse,
        HTTPStatus.CREATED.value
    )
    def post(self, file: UploadFile = File(...)):
        try:
            workflow_file = file.file.read()
            workflow_data = json.loads(workflow_file.decode('utf8').replace("'", '"'))
            process_result = WorkFlowController.process_workflow(workflow=WorkFlow(**workflow_data))
            return process_result
        except JSONDecodeError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail="Invalid format, details: {}".format(e)
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Unexpected server error. Details: {}".format(e)
            )
