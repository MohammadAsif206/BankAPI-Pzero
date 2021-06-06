from abc import ABC

from exceptions.resource_not_found import ResourceNotFound
from typing import List
from daos.account_dao import AccountDAO
from entities.account import Account
from exceptions.invalid_prameter import InvalidParameter


# AccountDAO that saves objects in local memory
class AccountDaoLocal(AccountDAO):
    account_number_maker = 0  # mimics a primary key generator in a database
    account_table = {}  # a dictionary, it mimics a table in a database

    def create_account(self, account: Account) -> Account:
        AccountDaoLocal.account_number_maker += 1
        account.account_number = AccountDaoLocal.account_number_maker
        # adding a new item to a dictionary
        AccountDaoLocal.account_table[AccountDaoLocal.account_number_maker] = account
        return account

    def get_account_by_id(self, account_number: int) -> Account:
        account = AccountDaoLocal.account_table.get(account_number)
        if account is None:
            raise ResourceNotFound(f" Invalid or nonexistent account number: {account_number}")
        return account

    def get_all_accounts(self) -> List[Account]:
        account_list = list(AccountDaoLocal.account_table.values())
        return account_list

    def update_account(self, account: Account) -> Account:
        if AccountDaoLocal.account_table.get(account.account_number) is None:
            raise ResourceNotFound(f"Invalid or nonexistent account number {account.account_number}")
        AccountDaoLocal.account_table[account.account_number] = account
        return account

    def delete_account(self, account_number: int) -> bool:
        if AccountDaoLocal.account_table.get(account_number) is None:
            raise ResourceNotFound(f" Invalid or nonexistent account number: {account_number}")

        del AccountDaoLocal.account_table[account_number]
        return True
