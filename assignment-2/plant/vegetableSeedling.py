from plant.plant import Plant

class VegetableSeedling(Plant):
    """
    A Class for documenting details of VegetableSeedling
    This class inherits all attributes and methods from Plant class
    Category needs to return through here because category is a abstract method in plant.py

    Args:
        seedlings_per_punnet (int)

    Attributes:
        __seedlings_per_punnet (int): number of seedlings per punnet
    """
    def __init__(self, id: int, name: str, price: float, stock_level: int, seedlings_per_punnet: int = 6) -> None:
        super().__init__(id, name, price, stock_level)
        self.__seedlings_per_punnet = seedlings_per_punnet

    def __str__(self):
        """Return a readable, multi-line summary of the plant."""
        return super().__str__() + f"\nSeedlings per punnet: {self.__seedlings_per_punnet}"

    @property
    def category(self) -> str:
        """Return the category of the plant"""
        return "Vegetable Seedling"

    @property
    def unit_label(self) -> str:
        """Return the unit label of the plant"""
        return "punnet"

    @property
    def seedlings_per_punnet(self) -> int:
        """Return the seedlings of per punnet"""
        return self.__seedlings_per_punnet
