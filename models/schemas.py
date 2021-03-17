from typing import List, Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.schema import datetime


class AccountCreate(BaseModel):
    user_id: str
    pin: int
    balance: Optional[int]


class Account(AccountCreate):

    class Config:
        arbitrary_types_allowed = True


class AccountValid(BaseModel):
    id: str
    is_valid: str


class Condition(BaseModel):
    from_id: str
    field_id: str
    operator: str
    value: Any


class Transition(BaseModel):
    target: str
    condition: Optional[List[Condition]]


class Trigger(BaseModel):
    id: str
    params: dict
    transitions: List[Transition]


class Step(BaseModel):
    id: str
    action: str
    params: dict
    transitions: List[Transition]
    workflow_execution_id: Optional[ObjectId]
    id_: Optional[ObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True


class StepResult(BaseModel):

    step_id: str
    workflow_execution_id: str
    id: Optional[ObjectId] = Field(alias="_id")
    result: Optional[dict]
    create_date: datetime

    class Config:
        arbitrary_types_allowed = True


class WorkFlow(BaseModel):
    trigger: Trigger
    steps: List[Step]


class WorkflowExecution(BaseModel):
    trigger: Trigger
    id: Optional[ObjectId] = Field(alias="_id")
    current_params: Optional[dict]
    last_action: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class WorkflowSuccessResponse(BaseModel):
    message: str



