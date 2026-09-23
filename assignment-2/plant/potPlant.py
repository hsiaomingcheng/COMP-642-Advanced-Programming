from plant.plant import Plant

class PotPlant(Plant):
    """
    A Class for documenting details of Pot Plant
    This class inherits all attributes and methods from Plant class
    Category needs to return through here because category is a abstract method in plant.py

    Args:
        size (str)

    Attributes:
        __size (str): size of the Pot Plant
    """
    def __init__(self, id: int, name: str, price: float, stock_level: int, size: str) -> None:
        """
        Create a Pot Plant.

        Raises:
            ValueError: if the size value is invalid
        """
        if size not in ("small", "medium", "large"):
            raise ValueError("Please enter valid size of plant")

        super().__init__(id, name, price, stock_level)
        self.__size = size

    def __str__(self):
        """Return a readable, multi-line summary of the plant."""
        return super().__str__() + f"\nSize: {self.__size}"

    @property
    def category(self) -> str:
        """Return the category of the plant"""
        return "Pot Plant"

    @property
    def unit_label(self) -> str:
        """Return the unit label of the plant"""
        return "pot"

    @property
    def size(self) -> str:
        """Return the size of the Pot Plant"""
        return self.__size
