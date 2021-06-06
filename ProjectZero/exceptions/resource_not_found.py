
class ResourceNotFound(Exception):
    description: str = "Occurs when a customer with a specific Id does not exist"

    def __str__(self):
        return "The requested resource not found"