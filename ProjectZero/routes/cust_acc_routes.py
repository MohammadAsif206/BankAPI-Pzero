
from flask import Flask, request, jsonify
from werkzeug.exceptions import abort

from entities.customer import Customer
from daos.customer_dao import CustomerDAO
from daos.customer_dao_local import CustomerDaoLocal
from daos.customer_dao_postgres import CustomerDaoPostgres
from services.customer_service_impl import CustomerServiceImpl

from exceptions.resource_not_found import ResourceNotFound
from exceptions.invalid_prameter import InvalidParameter
from exceptions.insufficient_fund import InsufficientFund

from entities.account import Account
from daos.account_dao import AccountDAO
from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from services.account_service_impl import AccountServiceImpl

customer_dao = CustomerDaoPostgres()
# customer_dao = CustomerDaoLocal
customer_service = CustomerServiceImpl(customer_dao)

account_dao = AccountDaoPostgres()
account_service = AccountServiceImpl(account_dao, customer_dao)


def create_routes(app: Flask):
    @app.route("/clients", methods=["POST"])
    def create_customer():
        body = request.json
        customer = Customer(body["customerId"], body["firstName"], body["lastName"], body["phoneNumber"],
                            body["emailAddress"], body["address"])
        customer_service.create_customer(customer)
        app.logger.info(f"Created customer with the ID of {customer.customer_id}")
        return jsonify(customer.as_json_dic()), 201

    @app.route("/clients", methods=["GET"])
    def get_all_customers():
        try:
            customers = customer_service.retrieve_all_customers()
            if customers is not None:
                jsonized_customers = [c.as_json_dic() for c in customers]
                return jsonify(jsonized_customers), 200
        except ResourceNotFound as e:
            return str(e), 404

    @app.route("/clients/<customer_id>", methods=["GET"])
    def get_customer_by_id(customer_id: str):
        if not customer_id.isnumeric():
            raise InvalidParameter
        else:
            try:
                customer = customer_service.retrieve_customer_by_id(int(customer_id))
                return jsonify(customer.as_json_dic()), 200
            except ResourceNotFound as e:
                return str(e), 404
            except InvalidParameter as e:
                return str(e), 404

    @app.route("/clients/<customer_id>", methods=["PUT"])
    def put_customer(customer_id: str):
        if not customer_id.isnumeric():
            raise InvalidParameter
        try:
            body = request.json
            customer = Customer(body["customerId"], body["firstName"], body["lastName"], body["phoneNumber"],
                                body["emailAddress"], body["address"])
            customer.customer_id = int(customer_id)
            customer_service.update_customer(customer)
            return jsonify(customer.as_json_dic()), 200
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients/<customer_id>", methods=["DELETE"])
    def del_customer(customer_id: str):
        if not customer_id.isnumeric():
            raise InvalidParameter
        else:
            try:
                customer_service.delete_customer(int(customer_id))
                app.logger.info(f" Deleted customer with the ID: {customer_id}")
                return "Deleted successfully ", 205
            except ResourceNotFound as e:
                return str(e), 404
            except InvalidParameter as e:
                return str(e), 404

    # -----------------------------------------------------------------------------------------------------
    @app.route("/accounts/customer_id/<customer_id>", methods=["POST"])
    def create_account(customer_id: str):
        try:
            if not customer_id.isnumeric():
                raise InvalidParameter
            body = request.json  # json will return a py dictionary version of that JSON
            account = Account(body["accountNumber"], body["accountBalance"], body["accountType"], int(customer_id))
            account_service.create_account_by_customer_id(account,
                                                          int(customer_id))  # pass the heavier logic to the service
            app.logger.info(f"new account created with ID: {account.account_number}")
            return jsonify(account.as_jason_dic()), 201
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/accounts/<customer_id>", methods=["GET"])
    def get_account_by_cid(customer_id: str):
        try:
            if not customer_id.isnumeric():
                raise InvalidParameter
            all_accounts = account_service.retrieve_all_accounts_by_cid(int(customer_id))
            app.logger.info(f"Total number of accounts for the customer with ID: {customer_id} ")
            return jsonify([account.as_jason_dic() for account in all_accounts])
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients/<customer_id>/upper_limit/<upper_limit>/lower_limit/<lower_limit>", methods=["GET"])
    def get_accounts_by_cid_and_balance_range(customer_id: str, lower_limit: str, upper_limit: str):
        try:
            if not (customer_id.isnumeric() and lower_limit.isnumeric() and upper_limit.isnumeric()):
                raise InvalidParameter
            all_accounts = account_service.retrieve_account_by_cid_and_balance_range(int(customer_id), int(lower_limit),
                                                                                     int(upper_limit))
            app.logger.info(
                f" The accounts of customer with ID: {customer_id} having more than {lower_limit} and less than {upper_limit}")
            return jsonify([account.as_jason_dic() for account in all_accounts])
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients/customer_id/<customer_id>/account_number/<account_number>", methods=["GET"])
    def get_account_by_customer_and_account_ids(customer_id: str, account_number: str):
        try:
            if not (customer_id.isnumeric() and account_number.isnumeric()):
                raise InvalidParameter
            account = account_service.retrieve_account_by_cid_and_aid(int(customer_id), int(account_number))
            app.logger.info(f"get account with customer id: {customer_id}, account number: {account_number}")
            return jsonify(account.as_jason_dic())
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients/customer_id/<customer_id>/account_id/<account_number>", methods=["PUT"])
    def put_account_by_cid_and_aid(customer_id: str, account_number: str):
        try:
            if not (customer_id.isnumeric() and account_number.isnumeric()):
                raise InvalidParameter
            account = Account.deserialized(request.json)
            account = account_service.update_account_by_cid_and_aid(account, int(customer_id), int(account_number))
            app.logger.info(
                f" The account with ID {account_number}, for customer with ID: {customer_id} updated successfully")
            return jsonify(account.as_jason_dic())
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients//<customer_id>/accounts/<account_number>", methods=["DELETE"])
    def delete_account_using_cid_and_aid(customer_id: str, account_number: str):
        if not (customer_id.isnumeric() and account_number.isnumeric()):
            raise InvalidParameter
        try:
            account_service.delete_account_by_cid_and_aid(int(customer_id), int(account_number))
            app.logger.info(f"The account with ID: {account_number} deleted successfully.")
            return True
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404

    @app.route("/clients/<customer_id>/accounts/<account_number>", methods=["PATCH"])
    def deposit_withdraw_by_cid_and_aid(customer_id: str, account_number: str):
        try:
            if not (customer_id.isnumeric() and account_number.isnumeric()):
                raise InvalidParameter
            body = request.json
            deposit = 0
            withdraw = 0
            if "deposit" in body:
                deposit = float(body["deposit"])
            if "withdraw" in body:
                withdraw = float(body["withdraw"])
            account = account_service.do_trans_on_account_by_cid_and_aid(int(customer_id),
                                                                         int(account_number), withdraw, deposit)
            app.logger.info(f"Requested transaction by customer with ID: {customer_id} on account with ID "
                            f"{account_number} successfully done")
            return jsonify(account.as_jason_dic())
        except InvalidParameter as e:
            return str(e), 404
        except ResourceNotFound as e:
            return str(e), 404
        except InsufficientFund as e:
            return str(e), 422

    @app.route("/clients/account/<s_account_number>/account/<r_account_number>", methods=["PATCH"])
    def transfer_fund_between_accounts_of_client(s_account_number: str, r_account_number: str):
        try:
            if not (s_account_number.isnumeric() and r_account_number.isnumeric()):
                raise InvalidParameter
            body = request.json
            amount = body["amount"]
            transfered = account_service.transfer_fund_between_account_of_a_client_by_aids(int(s_account_number),
                                                                                           int(r_account_number),
                                                                                           float(amount))
            app.logger.info(f"Transfer transaction between account {s_account_number} and"
                            f"{r_account_number} completed successfully")
            return jsonify([account.as_jason_dic() for account in transfered])
        except ResourceNotFound as e:
            return str(e), 404
        except InvalidParameter as e:
            return str(e), 404
        except InsufficientFund as e:
            return str(e), 422
# --------------------------------------End of cust_acc_routes module @line 220------------- ----
