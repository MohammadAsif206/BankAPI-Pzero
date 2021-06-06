from typing import List
from entities.customer import Customer
from daos.customer_dao import CustomerDAO
from exceptions.resource_not_found import ResourceNotFound


class CustomerDaoLocal(CustomerDAO):
    customer_id_maker = 0  # this mimics a primary key generator in a database
    customer_table = {}  # a dictionary mimicing a table in a database

    def create_customer(self, customer: Customer) -> Customer:
        CustomerDaoLocal.customer_id_maker += 1
        customer.customer_id = CustomerDaoLocal.customer_id_maker
        CustomerDaoLocal.customer_table[CustomerDaoLocal.customer_id_maker] = customer
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:

        customer = CustomerDaoLocal.customer_table.get(customer_id)
        if customer is None:
            raise ResourceNotFound(f"Invalid or nonexistent customer id: {customer_id}")
        return customer

    def get_all_customers(self) -> List[Customer]:
        all_customers = list(CustomerDaoLocal.customer_table.values())
        return all_customers

    def update_customer(self, customer: Customer) -> Customer:
        if CustomerDaoLocal.customer_table.get(customer.customer_id) is None:
            raise ResourceNotFound(f"Invalid or nonexistent customer Id: {customer.customer_id}")
        CustomerDaoLocal.customer_table[customer.customer_id] = customer
        return customer

    def delete_customer(self, customer_id: int) -> bool:
        if CustomerDaoLocal.customer_table.get(customer_id) is None:
            raise ResourceNotFound(f"Invalid or nonexistent customer Id: {customer_id}")
        del CustomerDaoLocal.customer_table[customer_id]
        return True
