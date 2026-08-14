class Plant:
    """
    A Class for documenting details of plants

    Args:
        id (int)
        name (str)
        category (str)
        price (int)
        stockLevel (int)

    Attributes:
        __plantId (int): serial number of plants
        __plantName (str): name of the plant
        __plantCategory (str): options of category (trees and shrubs, perennials, pot plants, or vegetable seedlings)
        __plantPrice (int): price of the plant
        __plantStockLevel (int): the amount of the plant been stocked
    """

    def __init__(self, id: int, name: str, category: str, price: int, stockLevel: int):

        # prevent a plant object with negative price
        if price < 0:
            raise ValueError("Plant price cannot be negative.")

        self.__plantId = id
        self.__plantName = name
        self.__plantCategory = category
        self.__plantPrice = price
        self.__plantStockLevel = stockLevel

    def __str__(self):
        return f"Plant id: {self.__plantId}\nPlant name: {self.__plantName}\nPlant Category: {self.__plantCategory}\nPrice: {self.__plantPrice}\nStock level: {self.__plantStockLevel}"

    @property
    def id(self):
        return self.__plantId

    @property
    def name(self):
        return self.__plantName

    @property
    def plantPrice(self):
        return self.__plantPrice

    @property
    def stockLevel(self):
        return self.__plantStockLevel

    @stockLevel.setter
    def stockLevel(self, amount: int):
        self.__plantStockLevel += amount

    def stockLevelCheckAndBuy(self, amount: int):
        if self.stockLevelCheck(amount):
            self.__plantStockLevel = self.__plantStockLevel - amount
        else:
            raise ValueError("The plant's stock level is not enough.")

    def stockLevelCheck(self, amount: int) -> bool:
        return self.__plantStockLevel >= amount
