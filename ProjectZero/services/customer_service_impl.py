
from entities.customer import Customer
from daos.customer_dao import CustomerDAO
from services.customer_service import  CustomerService

class CustomerServiceImpl(CustomerService):

    def __init__(self, customer_dao: CustomerDAO):
        self.customer_dao = customer_dao

    def create_customer(self, customer: Customer):
        return self.customer_dao.create_customer(customer)

    def retrieve_all_customers(self):
        return self.customer_dao.get_all_customers()

    def retrieve_customer_by_id(self, customer_id: int):
        return self.customer_dao.get_customer_by_id(customer_id)

    def update_customer(self, customer: Customer):
        return self.customer_dao.update_customer(customer)

    def delete_customer(self, customer_id: Customer):
        return self.customer_dao.delete_customer(customer_id)



