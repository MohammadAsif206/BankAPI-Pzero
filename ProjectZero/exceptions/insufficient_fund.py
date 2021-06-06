class InsufficientFund(Exception):
    def __str__(self):
        return "Insufficient funds, your requested withdraw or transfer is greater than the balance available."