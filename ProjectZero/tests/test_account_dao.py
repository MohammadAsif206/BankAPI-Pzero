
from entities.account import Account
from daos.account_dao import AccountDAO
from unittest import TestCase
from daos.account_dao_local import AccountDaoLocal
from exceptions.resource_not_found import ResourceNotFound
from daos.account_dao_postgres import AccountDaoPostgres
from entities.customer import Customer
from daos.customer_dao import CustomerDAO
from daos.customer_dao_postgres import CustomerDaoPostgres
from daos.customer_dao_local import CustomerDaoLocal

account_dao: AccountDAO = AccountDaoPostgres()
#account_dao: AccountDAO = AccountDaoLocal()
customer_dao: CustomerDAO = CustomerDaoPostgres()
#customer_dao: CustomerDAO = CustomerDaoLocal()
# An entity that has not been saved should have an id of 0
# This is the well established convention in every tech stack
# Many applications store data information as the unix epoch
# Seconds from Jan 1st midnight 1970

test_customer = Customer(0, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 Wes Lane")
customer_dao.create_customer(test_customer)
test_account = Account(0, 100.0, "Saving", 0)
test_account1 = Account(-1, 100.0, "Saving", 3)



# Pytest runs tests in order from top to bottom
def test_create_account():
    test_account.customer_id = test_customer.customer_id
    account_dao.create_account(test_account)
    assert test_account.account_number != 0


def test_get_account_by_id():
    test_account = account_dao.create_account(test_account)
    result = account_dao.get_account_by_aid(test_account.account_number)

    # result = account_dao.get_account_by_id(test_account.account_number)
    TestCase().assertDictEqual(result.as_jason_dic(), account_number.as_jason_dic())


def test_get_account_by_id_fail():
    try:
        account_dao.get_account_by_aid(-1)
        assert False
    except ResourceNotFound:
        assert True


def test_delete_account_by_id():
    account = account_dao.create_account(test_account)
    assert account_dao.delete_account(account.account_number)
    try:
        account_dao.get_account_by_id(account.account_number)
        assert False
    except ResourceNotFound:
        assert True


def test_update_account():
    account = account_dao.create_account(test_account)
    account.account_type = "CheckingSave"
    updated_account = account_dao.update_account(test_account)
    assert updated_account == account_dao.create_account(test_account)


def test_update_account_fail():
    try:
        account_dao.update_account(test_account1)
        assert False
    except ResourceNotFound:
        assert True
