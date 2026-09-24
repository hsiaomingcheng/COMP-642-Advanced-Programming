from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plant.plant import Plant

class OrderItem:
    """
    To document the item details of the item from order.

    Args:
        plant (Plant): plant object.
        quantity (int): the quantity for the plant.

    Attributes:
        __plant (Plant): plant object.
        __quantity (int): quantity for punnet/pot/plant.
    """

    DISCOUNT_THRESHOLD = 10
    DISCOUNT_RATE = 0.1

    def __init__(self, plant: "Plant", quantity: int) -> None:
        """
        Create OrderItem object
        """
        if not isinstance(quantity, int):
            raise ValueError("The quantity must be an integer")

        if quantity <= 0:
            raise ValueError("The quantity cannot be 0 or less than 0")

        self.__plant = plant
        self.__quantity = quantity

    def __str__(self) -> str:
        """Return a readable summary of the order item."""
        plant_name = self.plant.name
        plant_quantity = self.__quantity
        plant_unit = self.plant.unit_label
        plant_item_total_price = self.get_cost()
        return f"Plant Name: {plant_name}, Quantity: {plant_quantity}/{plant_unit}, Total Price: {plant_item_total_price}"

    @property
    def plant(self) -> "Plant":
        """return plant object"""
        return self.__plant

    @property
    def quantity(self) -> int:
        """return the quantity of the order"""
        return self.__quantity

    def get_cost(self) -> float:
        """
        Calculate the item total, applying a 10% discount when 10 or more
        units are purchased.

        Returns:
            float: the item's total price.
        """
        total_price = self.quantity * self.plant.plant_price

        if self.quantity >= self.DISCOUNT_THRESHOLD:
            total_price = total_price * (1 - self.DISCOUNT_RATE)

        return round(total_price, 2)

    def add_quantity(self, amount: int) -> None:
        """Adding extra quantity to the order."""
        if not isinstance(amount, int):
            raise ValueError("The amount must be an integer")

        if amount <= 0:
            raise ValueError("The amount must be greater than 0")

        self.__quantity += amount

    def check_stock(self) -> bool:
        """Checking the stock level of the plant."""
        return self.plant.stock_level_check(self.__quantity)

    def reserve_stock(self) -> None:
        """Reducing the stock number."""
        self.plant.stock_level_check_and_buy(self.__quantity)

    def return_stock(self) -> None:
        """return the stock number back to the plant."""
        self.plant.add_stock(self.__quantity)
