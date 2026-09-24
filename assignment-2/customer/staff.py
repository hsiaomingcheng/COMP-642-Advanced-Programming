from customer.customer import Customer

class Staff(Customer):
    """
    A Class for documenting details of Staff
    This class inherits all attributes and methods from Customer class

    It has two new getters, customer_type and discount_rate
    """
    def __init__(self, id: int, name: str, email: str, phone_number: str, balance: float = 0) -> None:
        """
        Create a Staff object.
        """
        super().__init__(id, name, email, phone_number, balance)

    @property
    def customer_type(self) -> str:
        """str: return Staff as the type of customer"""
        return "Staff"

    @property
    def discount_rate(self) -> float:
        """float: return the discount rate for staff customer"""
        return 0.01
