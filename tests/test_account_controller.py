import unittest
from unittest.mock import Mock, patch

import mongomock

import settings
from controllers.account import AccountController
from models.schemas import AccountCreate
from repositories.account import AccountRepository
from settings import MongoSettings


class TestAccount(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.user_id = '1000001'
        cls.pin = 1233

    @mongomock.patch(servers=(('mongodb+srv://cluster0.oyz87.mongodb.net', 27017),))
    def test_user_creation(self):
        account = AccountCreate(user_id=self.user_id, pin=self.pin, balance=20000)
        AccountController.create_account(account_create=account)
        saved_account = AccountRepository.get_account({'user_id': self.user_id})
        self.assertEqual(self.pin, saved_account.pin)

    @mongomock.patch(servers=(('cluster0.oyz87.mongodb.net', 27017),))
    def test_account_balance(self):
        account = AccountCreate(user_id=self.user_id, pin=self.pin, balance=20000)
        AccountController.create_account(account_create=account)
        balance = AccountController.get_account_balance(user_id=self.user_id)
        self.assertEqual(account.balance, balance.get('balance'))

    def test_deposit_transaction(self):
        account = AccountCreate(user_id=self.user_id, pin=self.pin, balance=20000)
        AccountController.create_account(account_create=account)
        balance = AccountController.get_account_balance(user_id=self.user_id)
        self.assertEqual(account.balance, balance.get('balance'))
        AccountController.deposit_money(self.user_id, money=5000)
        balance = AccountController.get_account_balance(user_id=self.user_id)
        self.assertEqual(account.balance + 5000, balance.get('balance'))
        mongomock.MongoClient().drop_database()

    @mongomock.patch(servers=(('mongodb+srv://playvox:playvox@cluster0.oyz87.mongodb.net')))
    def test_withdraw_transaction(self):
        account = AccountCreate(user_id=self.user_id, pin=self.pin, balance=20000)
        AccountController.create_account(account_create=account)
        balance = AccountController.get_account_balance(user_id=self.user_id)
        self.assertEqual(account.balance, balance.get('balance'))
        AccountController.withdraw(self.user_id, money=5000)
        balance = AccountController.get_account_balance(user_id=self.user_id)
        self.assertEqual(account.balance - 5000, balance.get('balance'))

