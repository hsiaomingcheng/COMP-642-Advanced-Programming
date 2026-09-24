from abc import ABC, abstractmethod
from nurseryErrorException import InsufficientStockError

class Plant(ABC):
    """
    A Class for documenting details of plants

    Args:
        id (int)
        name (str)
        price (float): must be 0 or greater; 0 represents a free plant.
        stock_level (int)

    Attributes:
        __plant_id (int): serial number of plants
        __plant_name (str): name of the plant
        __plant_price (float): price of the plant, 0 means the plant is free
        __plant_stock_level (int): the amount of the plant been stocked
    """

    def __init__(self, id: int, name: str, price: float, stock_level: int) -> None:
        """
        Create a plant.

        Raises:
            ValueError: if price is negative
        """
        # price must be a positive float, 0 is allowed to represent a free plant
        if price < 0:
            raise ValueError("Plant price cannot be negative.")

        self.__plant_id = id
        self.__plant_name = name
        self.__plant_price = float(price)
        self.__plant_stock_level = stock_level

    def __str__(self) -> str:
        """Return a readable, multi-line summary of the plant."""
        price_display = "Free" if self.__plant_price == 0 else self.__plant_price
        return (
            f"Plant:\n"
            f"Plant id: {self.__plant_id}\n"
            f"Plant name: {self.__plant_name}\n"
            f"Plant Category: {self.category}\n"
            f"Price: {price_display}\n"
            f"Stock level: {self.__plant_stock_level}\n"
            f"Unit label: {self.unit_label}"
        )

    @property
    def unit_label(self) -> str:
        """Return a default unit label, if the child class does not provide one."""
        return "plant"

    @property
    def id(self) -> int:
        """int: the plant's id."""
        return self.__plant_id

    @property
    def name(self) -> str:
        """str: the plant's name."""
        return self.__plant_name

    @property
    @abstractmethod
    def category(self) -> str:
        """force child class to pass their own category when they trying to build a object."""
        pass

    @property
    def plant_price(self) -> float:
        """float: the plant's price; 0 means the plant is free."""
        return self.__plant_price

    @plant_price.setter
    def plant_price(self, new_price: float) -> None:
        """
        Update the plant's price.

        Raises:
            ValueError: if new_price is negative.
        """
        # price must be a positive float, 0 is allowed to represent a free plant
        if new_price < 0:
            raise ValueError("Plant price cannot be negative.")

        self.__plant_price = float(new_price)

    @property
    def stock_level(self) -> int:
        """int: the plant's current stock level."""
        return self.__plant_stock_level

    def add_stock(self, amount: int) -> None:
        """
        Restock the plant by adding to its stock level.

        Args:
            amount (int): number of units to add, must be greater than 0.

        Raises:
            ValueError: if amount is not greater than 0.
        """
        # restocking must add a positive amount
        if amount <= 0:
            raise ValueError("The amount to add must be greater than 0.")

        self.__plant_stock_level += amount

    def stock_level_check_and_buy(self, amount: int) -> None:
        """
        Reduce the plant's stock level by amount, if enough stock is available.

        Args:
            amount (int): number of units being purchased.

        Raises:
            ValueError: if there is not enough stock.
        """
        if self.stock_level_check(amount):
            self.__plant_stock_level = self.__plant_stock_level - amount
        else:
            raise InsufficientStockError("The plant's stock level is not enough.")

    def stock_level_check(self, amount: int) -> bool:
        """Return True if the plant's stock level is at least amount."""
        return self.__plant_stock_level >= amount
