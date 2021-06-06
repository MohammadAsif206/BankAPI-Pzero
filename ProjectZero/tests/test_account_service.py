from unittest.mock import MagicMock

from daos.account_dao import AccountDao
from daos.account_dao_postgres import AccountDaoPostgres
from daos.customer_dao import CustomerDao
from daos.customer_dao_postgres import CustomerDaoPostgres
from entities.account import Account
from entities.customer import Customer
from exceptions.resource_not_found import ResourceNotFound
from service.account_service import AccountService
from service.account_service_impl import AccountServiceImpl

customer_dao: CustomerDao = CustomerDaoPostgres()
account_dao: AccountDao = AccountDaoPostgres()
account_service: AccountService = AccountServiceImpl(account_dao, customer_dao)

test_customer: Customer = Customer(1, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 Wes Lane")
test_customer3: Customer = Customer(-1, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 Wes Lane")


customer_dao.create_customer(test_customer)
test_account: Account = Account(0,  1000, "checking", test_customer.customer_id)
account_dao.create_account(test_account)

account_dao.get_account_by_cid_and_aid = MagicMock(return_value=test_account)


class TestAccountService:
    def test_do_trans_on_account_by_cid_and_aid(self):
        account = account_service.do_trans_on_account_by_cid_and_aid(test_account.customer_id,
                                                                     test_account.account_number, 0, 500)

        assert account.balance == test_account.account_balance

    def test_do_trans_on_account_by_cid_and_aid(self):
        try:
            account_service.do_trans_on_account_by_cid_and_aid(test_account.customer_id,
                                                               test_account.account_number, 0, 500)
            assert False
        except ResourceNotFound:
            pass

    def test_transfer_fund_between_account_of_a_client_by_aids(self):
        account1 = account_dao.create_account(test_account)
        account2 = account_dao.create_account(test_account)
        print(account1)
        print(account2)
        accounts = account_service.transfer_fund_between_account_of_a_client_by_aids(
            account1.account_number, account2.account_number, 100)

        assert (accounts[1].balance - account1.balance) == 100

    def test_transfer_fund_between_account_of_a_client_by_aids(self):
        try:
            account_service.transfer_fund_between_account_of_a_client_by_aids(
                0, test_account.account_number, 1000)
            assert False
        except ResourceNotFound:
            pass


