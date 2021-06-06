from typing import List
from daos.account_dao import AccountDAO
from entities.account import Account
from utils.connection_util import connection
from exceptions.resource_not_found import ResourceNotFound


class AccountDaoPostgres(AccountDAO):

    def create_account_by_customer_id(self, account: Account, customer_id: int) -> Account:
        sql = """insert into account (account_balance, account_type, customer_id)
                values(%s,%s,%s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_balance, account.account_type, customer_id))
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        account.account_number = record[0]
        return account

    def create_account(self, account: Account) -> Account:
        sql = """insert into account (account_balance, account_type, customer_id)
                values(%s,%s,%s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_balance, account.account_type, customer_id))
        connection.commit()
        account.account_number = cursor.fetchone()[0]
        return account

    def get_all_accounts_by_cid(self, customer_id: int) -> list[Account]:
        sql = """select * from account where customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        all_accounts = cursor.fetchall()
        accounts = [Account(*an_account) for an_account in all_accounts]
        if len(accounts) == 0:
            raise ResourceNotFound
        return accounts

    def get_account_by_cid_and_balance_range(self, customer_id: int, lower_limit: int, upper_limit: int) -> [Account]:
        sql = """select * from account where customer_id = %s and account_balance between %s and %s """
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, lower_limit, upper_limit])
        balance_range = cursor.fetchall()
        if balance_range is None:
            raise ResourceNotFound
        accounts = [Account(*b_range) for b_range in balance_range]
        return accounts

    def get_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> Account:
        sql = """select * from account where customer_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, account_number])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        account = Account(*record)
        return account

    def update_account_by_cid_and_aid(self, account: Account, customer_id: int, account_number: int) -> Account:
        sql = """update account set account_balance = %s, account_type = %s where customer_id = %s and account_id = %s
        returning account_id, customer_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [account.account_balance, account.account_type, customer_id, account_number])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        account.account_number = record[0]
        account.customer_id = record[1]
        return account

    def delete_account_by_cid_and_aid(self, customer_id: int, account_number: int) -> bool:
        sql = """delete from account where customer_id = %s and account_id = %s returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, account_number])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        return True

    def delete_account_by_cid(self, customer_id: int) -> bool:
        pass

    def get_account_by_aid(self, account_number: int) -> Account:
        sql = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_number])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        account = Account(*record)
        return account

    def update_account_balance_by_aid(self, account_balance: float, account_number: int) -> bool:
        sql = """update account set account_balance = %s where account_id = %s returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_balance, account_number])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound
        return True
