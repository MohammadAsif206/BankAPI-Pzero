
from abc import ABC, abstractmethod
from entities.account import Account


class AccountService(ABC):
    # General CRUD functionality
    @abstractmethod
    def create_account_by_customer_id(self, account: Account, customer_id: int):
        pass
    @abstractmethod
    def retrieve_all_accounts_by_cid(self, customer_id: int) -> list[Account]:
        pass

    @abstractmethod
    def retrieve_account_by_cid_and_balance_range(self, customer_id: int, lower_limit: float, upper_limit: float) ->[Account]:
        pass
    @abstractmethod
    def retrieve_account_by_cid_and_aid(self, customer_id: int, account_number: int) ->Account:
        pass
    @abstractmethod
    def update_account_by_cid_and_aid(self, account: Account, customer_id: int, account_number: int) -> Account:
        pass
    @abstractmethod
    def delete_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> bool:
        pass

    @abstractmethod
    def do_trans_on_account_by_cid_and_aid(self, customer_id: int, account_number: int,
                                           withdraw: float, deposit: float) -> Account:
        pass

    @abstractmethod
    def transfer_fund_between_account_of_a_client_by_aids(self, s_account_number: int, r_account_number: int,
                                                          amount: float) -> [Account]:
        pass


