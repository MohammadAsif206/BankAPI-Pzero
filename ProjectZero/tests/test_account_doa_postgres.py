
from unittest import TestCase
from entities.account import Account
from daos.account_dao import AccountDAO
from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from exceptions.resource_not_found import ResourceNotFound

account_dao: AccountDAO = AccountDaoPostgres

test_account = Account(1, 100.0, 3, "Saving")
test_account1 = Account(-1, 100.0, 3, "Saving")


def test_create_account():
    account_dao.create_account(test_account)
    assert test_account.account_number != 0
    pass
