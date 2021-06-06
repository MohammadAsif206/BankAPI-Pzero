
from daos.account_dao import AccountDAO
from services.account_service import AccountService
from entities.account import Account
from daos.customer_dao import CustomerDAO
from exceptions.insufficient_fund import InsufficientFund


class AccountServiceImpl(AccountService):
    # Composition
    def __init__(self, account_dao: AccountDAO, customer_dao: CustomerDAO):
        self.account_dao = account_dao
        self.customer_dao = customer_dao

    # POST /client/5/accounts create account for a specific customer
    def create_account_by_customer_id(self, account: Account, customer_id: int) -> Account:
        self.customer_dao.get_customer_by_id(customer_id)
        return self.account_dao.create_account_by_customer_id(account, customer_id)

    def retrieve_all_accounts_by_cid(self, customer_id: int) -> list[Account]:
        self.customer_dao.get_customer_by_id(customer_id)
        return self.account_dao.get_all_accounts_by_cid(customer_id)

    def retrieve_account_by_cid_and_balance_range(self, customer_id: int, lower_limit: float, upper_limit: float) -> [
        Account]:
        self.customer_dao.get_customer_by_id(customer_id)
        return self.account_dao.get_account_by_cid_and_balance_range(customer_id, lower_limit, upper_limit)

    def retrieve_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> Account:
        return self.account_dao.get_account_by_cid_and_aid(customer_id, account_number)

    def update_account_by_cid_and_aid(self, account: Account, customer_id: int, account_number: int) -> Account:
        return self.account_dao.update_account_by_cid_and_aid(account, customer_id, account_number)

    def delete_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> bool:
        self.account_dao.delete_account_by_cid_and_aid(customer_id, account_number)
        return True

    def do_trans_on_account_by_cid_and_aid(self, customer_id: int, account_number: int,
                                           withdraw: float, deposit: float) -> Account:
        account = self.account_dao.get_account_by_cid_and_aid(customer_id, account_number)
        if account.account_balance < (withdraw - deposit):
            raise InsufficientFund
        account.account_balance += (deposit - withdraw)
        return self.account_dao.update_account_by_cid_and_aid(account, customer_id, account_number )

    def transfer_fund_between_account_of_a_client_by_aids(self, s_account_number: int, r_account_number: int,
                                                          amount: float):
        s_account = self.account_dao.get_account_by_aid(s_account_number)
        r_account = self.account_dao.get_account_by_aid(r_account_number)
        if s_account.account_balance < amount:
            raise InsufficientFund
        s_account.account_balance -= amount
        r_account.account_balance += amount
        self.account_dao.update_account_balance_by_aid(s_account.account_balance, s_account_number)
        self.account_dao.update_account_balance_by_aid(r_account.account_balance, r_account_number)
        return [s_account, r_account]



