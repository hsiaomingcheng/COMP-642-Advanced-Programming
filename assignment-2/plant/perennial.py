from plant.plant import Plant

class Perennial(Plant):
    """
    A Class for documenting details of Perennial
    This class inherits all attributes and methods from Plant class
    Category needs to return through here because category is a abstract method in plant.py
    """
    def __init__(self, id: int, name: str, price: float, stock_level: int) -> None:
        """
        Create a Perennial.
        """
        super().__init__(id, name, price, stock_level)

    @property
    def category(self) -> str:
        """Return the category of the plant"""
        return "Perennial"
