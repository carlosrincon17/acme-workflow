from functools import wraps

from fastapi import HTTPException
from pymongo.errors import PyMongoError

from exceptions.work_flow_exception import WorkFlowException, StepNotFoundException, InsufficientFundsError, \
    UnauthorizedException
from models.schemas import Transition


def log_transition(function):
    @wraps(function)
    def wrapper(cls, transition: Transition):
        print("Validating transaction to target: ({})".format(transition.target))
        result = function(cls, transition)
        if result:
            print("""Starting the transition to target: ({})""".format(transition.target))
        return result

    return wrapper


def register_transaction_log(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        money = kwargs.get('amount') or 0
        type_transaction = 'deposits' if money > 0 else 'withdraw'
        result = function(*args, **kwargs)
        print("New transaction(user={}, type={}, amount: {}, new_balance={})".format(
            kwargs['filters'].get('user_id'), type_transaction, money, result.dict().get('balance'))
        )
        return result
    return wrapped


def process_exception(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (WorkFlowException, StepNotFoundException, InsufficientFundsError, UnauthorizedException) as we:
            raise HTTPException(status_code=500, detail=we.message)
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail="Unexpected error connecting to database.")
    return wrapper
