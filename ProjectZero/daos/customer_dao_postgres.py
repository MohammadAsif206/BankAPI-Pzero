from typing import List
from daos.customer_dao import CustomerDAO
from entities.customer import Customer
# This module is for CustomerDaoPostgres, since PY allows multip inheritance, I attempted to add AccountDaoPostgres to it
from utils.connection_util import connection
from exceptions.resource_not_found import ResourceNotFound
from exceptions.invalid_prameter import InvalidParameter


class CustomerDaoPostgres(CustomerDAO):

    def create_customer(self, customer: Customer) -> Customer:
        # returning customer_id, it will return the value of the newly generated key  in the database
        sql = """INSERT INTO customer(first_name,last_name,phone_number,email_address,address) 
            VALUES (%s,%s,%s,%s,%s) RETURNING customer_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (customer.first_name, customer.last_name, customer.phone_number,
                             customer.email, customer.address))
        connection.commit()  # make permanent the sql statement that were executed
        customer_id = cursor.fetchone()[0]
        customer.customer_id = customer_id
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        sql = """SELECT * FROM customer WHERE customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFound("Resource not found")
        # customer = Customer(record[0], record[1], record[2], record[3], record[4], record[5])
        # record is indexed into 5, which adds up to 6 indices while 5 attributes explicitly been inserted
        # The attribute at zero index is the auto-generated key
        customer = Customer(*record)  # this line of code is a short form of the code three line above it
        return customer

    def get_all_customers(self) -> List[Customer]:
        sql = """SELECT * FROM customer"""
        cursor = connection.cursor()
        cursor.execute(sql)
        all_customers = cursor.fetchall()
        if all_customers is None:
            raise ResourceNotFound("There are not resources available")
        customers = [Customer(*a_customer) for a_customer in all_customers]
        return customers

    def update_customer(self, customer: Customer) -> Customer:
        sql = """UPDATE customer SET first_name=%s,last_name=%s,phone_number=%s,email_address=%s,
        address=%s WHERE customer_id=%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer.first_name, customer.last_name,
                    customer.phone_number,customer.email, customer.address, customer.customer_id])
        connection.commit()
        if self.get_customer_by_id(customer.customer_id) is None:
            raise ResourceNotFound(f"Invalid or nonexistent customer Id {customer.customer_id}")
        return customer

    def delete_customer(self, customer_id: int) -> bool:
        if  self.get_customer_by_id(customer_id) is None:
            raise ResourceNotFound(f"Invalid or nonexistent customer Id {customer_id}")
        sql = """DELETE FROM customer WHERE customer_id=%s;"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        connection.commit()
        return True

