class InvalidParameter(Exception):
    description: str = "Occurs when an account with a specific Id does not exist"

    def __str__(self):
        return "Invalid parameter,probably a non-numeric value entered"