from http import HTTPStatus
from fastapi_restful import Resource, set_responses

from models.schemas import Account, AccountCreate
from controllers.account import AccountController


class AccountApi(Resource):

    @set_responses(
        Account,
        HTTPStatus.CREATED.value
    )
    def post(self, account_create: AccountCreate):
        AccountController.create_account(account_create=account_create)
