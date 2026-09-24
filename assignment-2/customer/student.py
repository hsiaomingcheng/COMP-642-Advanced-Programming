from customer.customer import Customer

class Student(Customer):
    """
    A Class for documenting details of Student
    This class inherits all attributes and methods from Customer class

    It has two new getters, customer_type and discount_rate
    """
    def __init__(self, id: int, name: str, email: str, phone_number: str, balance: float = 0) -> None:
        """
        Create a Student object.
        """
        super().__init__(id, name, email, phone_number, balance)

    @property
    def customer_type(self) -> str:
        """str: return Student as the type of customer"""
        return "Student"

    @property
    def discount_rate(self) -> float:
        """float: return the discount rate for student customer"""
        return 0.05
