
from typing import List
from abc import ABC, abstractmethod
from entities.customer import Customer


class CustomerService(ABC):
    @abstractmethod
    def create_customer(self, customer: Customer):
        pass

    @abstractmethod
    def retrieve_all_customers(self):
        pass

    @abstractmethod
    def retrieve_customer_by_id(self, customer_id: int):
        pass

    @abstractmethod
    def update_customer(self, customer: Customer):
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int):
        pass
