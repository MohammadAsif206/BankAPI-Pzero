from typing import List
from abc import ABC, abstractmethod
from entities.account import Account


class AccountDAO(ABC):
    # CRUD
    # CREATE
    # create method SAVES a new account to a database or some other other locations
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_all_accounts_by_cid(self, customer_id: int) -> list[Account]:
        pass

    @abstractmethod
    def get_account_by_cid_and_balance_range(self, customer_id: int, lower_limit: float,
                                             upper_limit: float) -> [Account]:
        pass

    @abstractmethod
    def get_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> Account:
        pass

    @abstractmethod
    def update_account_by_cid_and_aid(self, account: Account, customer_id: int, account_number: int) -> Account:
        pass

    @abstractmethod
    def delete_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> bool:
        pass

    @abstractmethod
    def delete_account_by_cid(self, customer_id: int) -> bool:
        pass


    @abstractmethod
    def update_account_balance_by_aid(self, balance: float, account_number: int) -> bool:
        pass

    @abstractmethod
    def create_account_by_customer_id(self, account: Account, customer_id: int) -> Account:
        pass
    @abstractmethod
    def get_account_by_aid(self, account_number: int) -> Account:
        pass




