from plant.plant import Plant

class TreesAndShrubs(Plant):
    """
    A Class for documenting details of TreesAndShrubs
    This class inherits all attributes and methods from Plant class
    Category needs to return through here because category is a abstract method in plant.py
    """
    def __init__(self, id: int, name: str, price: float, stock_level: int) -> None:
        """
        Create a TreesAndShrubs.
        """
        super().__init__(id, name, price, stock_level)

    @property
    def category(self) -> str:
        """Return the category of the plant"""
        return "Trees and Shrubs"
