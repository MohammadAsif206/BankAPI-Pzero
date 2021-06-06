from unittest.mock import MagicMock
from unittest import TestCase
from entities.customer import Customer
from services.customer_service_impl import CustomerServiceImpl
from daos.customer_dao_postgres import CustomerDaoPostgres

from daos.customer_dao_local import CustomerDaoLocal


customers = [Customer(0, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 West Lane"),
             Customer(0, "Adin", "Jan", "2222222", "hotmail.com", " 21 East Lane"),
             Customer(0, "Majid", "Saif", "2222222", "hotmail.com", " 21 North Lane"),
             Customer(0, "Hasin", "Ojay", "2222222", "hotmail.com", " 21 South Lane")]

# the customer_service cannot work unless the CustomerDAO works correctly
mock_customer_dao = CustomerDaoPostgres
mock_customer_dao.get_all_customers = MagicMock(return_value=customers)
# if you cll this function that I magic mocked at line 18 return those four defined customers
customers = mock_customer_dao.get_all_customers()
customer_service = CustomerServiceImpl(mock_customer_dao)


def test_create_customer():
    id = '1'
    assert customer_service.retrieve_customer_by_id()
