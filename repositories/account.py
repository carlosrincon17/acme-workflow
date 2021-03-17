from bson import ObjectId

from models.schemas import AccountCreate, Account
from repositories.base_repository import BaseRepository
from util.decorators import register_transaction_log


class AccountRepository(BaseRepository):

    __collection__ = "accounts"

    @classmethod
    def create(cls, account_create: AccountCreate) -> Account:
        result = cls.get_collection().insert_one(account_create.dict())
        return cls.get_account({"_id": ObjectId(result.inserted_id)})

    @classmethod
    def get_account(cls, filters: dict) -> Account:
        account = cls.get_collection().find_one(filters)
        return Account(**account) if account else None

    @classmethod
    @register_transaction_log
    def update_balance(cls, filters: dict, amount: float):
        update_query = {"$inc": {"balance": amount}}
        cls.get_collection().update_one(filter=filters, update=update_query)
        return cls.get_account(filters=filters)
