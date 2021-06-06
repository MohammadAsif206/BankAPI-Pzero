class Account:

    def __init__(self, account_number: int, account_balance: float, account_type: str, customer_id: int):
        self.account_number = account_number
        self.account_balance = account_balance
        self.account_type = account_type
        self.customer_id = customer_id


    def __str__(self):
        return f"accountNumber={self.account_number}, Account Balance: $={self.account_balance}" \
               f" Account Type: ={self.account_type},  Account Holder: ={self.customer_id}"
    def as_jason_dic(self):
        return {
            "accountNumber": self.account_number,
            "accountBalance": self.account_balance,
            "accountType": self.account_type,
            "customerId": self.customer_id
        }
    @staticmethod
    def deserialized(as_jason_dic):
        account = Account(0, 0, "",0)
        account.account_number = as_jason_dic["accountNumber"]
        account.account_balance = as_jason_dic["accountBalance"]
        account.account_type = as_jason_dic["accountType"]
        account.customer_id = as_jason_dic["customerId"]
        return account



