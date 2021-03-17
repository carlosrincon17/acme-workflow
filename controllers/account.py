from exceptions.work_flow_exception import ActionNotFoundException, InsufficientFundsError
from models.schemas import AccountCreate, Account

from repositories.account import AccountRepository
from util.third_parties.trm import TRMHelper


class AccountController:

    def handle_action(self, action, **params):
        try:
            return getattr(self, action)(**params)
        except AttributeError as e:
            raise ActionNotFoundException(action=e)

    @classmethod
    def create_account(cls, account_create: AccountCreate) -> Account:
        return AccountRepository.create(account_create=account_create)

    @classmethod
    def validate_account(cls, **filters) -> dict:
        account = AccountRepository.get_account(filters=filters)
        print("Account validation Result: ({})".format('Is Valid' if account else 'is not valid'))
        return dict(is_valid=account is not None or False)

    @classmethod
    def get_account_balance(cls, user_id):
        filters = {'user_id': user_id}
        account = AccountRepository.get_account(filters=filters)
        print("Current account Balance: ({})".format(account.balance))
        return {'balance': account.balance}

    @classmethod
    def deposit_money(cls, user_id: str, money: float) -> dict:
        filters = {'user_id': user_id}
        account = AccountRepository.update_balance(filters=filters, amount=money)
        return {'balance': account.balance}

    @classmethod
    def withdraw_in_dollars(cls, user_id: str, money: float) -> dict:
        cop_money = TRMHelper.convert_usd_to_cop(usd_money=money)
        return cls.withdraw(user_id=user_id, money=cop_money)

    @classmethod
    def withdraw(cls, user_id: str, money: float) -> dict:
        filters = {'user_id': user_id}
        if AccountRepository.get_account(filters=filters).balance < money:
            raise InsufficientFundsError
        account = AccountRepository.update_balance(filters=filters, amount=-money)
        return {'balance': account.balance}

