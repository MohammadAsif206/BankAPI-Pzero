from entities.customer import Customer
from daos.customer_dao_local import CustomerDaoLocal
from daos.customer_dao import CustomerDAO
from unittest import TestCase
from exceptions.resource_not_found import ResourceNotFound

customer_dao: CustomerDAO = CustomerDaoLocal()
# An entity that has not been saved should have an id of 0
# This is the well established convention in every tech stack
# Many applications store data information as the unix epoch
# Seconds from Jan 1st midnight 1970

test_customer = Customer(1, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 Wes Lane")
test_customer3 = Customer(-1, "Mohammad", "Asif", "2222222", "hotmail.com", " 21 Wes Lane")


# Pytest runs tests in order from top to bottom
def test_create_customer():
    assert test_customer.customer_id != 0


def test_get_customer_by_id():
    customer_id = customer_dao.create_customer(test_customer)
    result = customer_dao.get_customer_by_id(test_customer.customer_id)
    TestCase().assertDictEqual(result.as_json_dic(), customer_id.as_json_dic())


def test_get_customer_by_id_fail():
    # customer_dao.get_customer_by_id()
    try:
        customer_dao.get_customer_by_id(-1)
        assert False
    except ResourceNotFound:
        assert True


def test_get_all_customer():
    result = customer_dao.get_all_customers()
    print(len(result))
    pass


def test_delete_customer_by_id():
    customer = customer_dao.create_customer(test_customer)
    assert customer_dao.delete_customer(customer.customer_id)
    try:
        customer_dao.get_customer_by_id(customer.customer_id)
        assert False
    except ResourceNotFound:
        assert True


def test_update_customer():
    customer = customer_dao.create_customer(test_customer)
    customer.first_name = " Ali"
    update_customer = customer_dao.update_customer(customer)
    assert update_customer.first_name == customer.first_name


def test_update_customer_fail():
    try:
        customer_dao.update_customer(test_customer3)
        assert False
    except ResourceNotFound:
        assert True
