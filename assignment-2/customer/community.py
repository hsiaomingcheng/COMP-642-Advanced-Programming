from customer.customer import Customer

class Community(Customer):
    """
    A Class for documenting details of Community
    This class inherits all attributes and methods from Customer class

    It has a new getters, customer_type.
    A new method to override the check_can_place_order from base class
    """
    def __init__(self, id: int, name: str, email: str, phone_number: str, balance: float = 0) -> None:
        """
        Create a Community object.
        """
        super().__init__(id, name, email, phone_number, balance)

    @property
    def customer_type(self) -> str:
        """str: return Community as the type of customer"""
        return "Community"

    def check_can_place_order(self, prospective_total: float) -> None:
        """Verify the customer's order status."""
        """preventing Community customer get second order before they collect their first order"""
        for order in self.orders:
            if order.status == "pending":
                raise ValueError(f"Customer {self.name} cannot place order because of the other pending orders.")
