class Plant:
    """
    A Class for documenting details of plants

    Args:
        id (int)
        name (str)
        category (str)
        price (float): must be 0 or greater; 0 represents a free plant.
        stock_level (int)

    Attributes:
        __plant_id (int): serial number of plants
        __plant_name (str): name of the plant
        __plant_category (str): options of category (trees and shrubs, perennials, pot plants, or vegetable seedlings)
        __plant_price (float): price of the plant, 0 means the plant is free
        __plant_stock_level (int): the amount of the plant been stocked
    """

    VALID_CATEGORIES = ("trees and shrubs", "perennials", "pot plants", "vegetable seedlings")

    def __init__(self, id: int, name: str, category: str, price: float, stock_level: int):

        # price must be a positive float, 0 is allowed to represent a free plant
        if price < 0:
            raise ValueError("Plant price cannot be negative.")

        # category must be one of the allowed options
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Plant category must be one of {self.VALID_CATEGORIES}.")

        self.__plant_id = id
        self.__plant_name = name
        self.__plant_category = category
        self.__plant_price = float(price)
        self.__plant_stock_level = stock_level

    def __str__(self):
        return f"Plant id: {self.__plant_id}\nPlant name: {self.__plant_name}\nPlant Category: {self.__plant_category}\nPrice: {self.__plant_price}\nStock level: {self.__plant_stock_level}"

    @property
    def id(self):
        return self.__plant_id

    @property
    def name(self):
        return self.__plant_name

    @property
    def category(self):
        return self.__plant_category

    @category.setter
    def category(self, new_category: str):
        # category must be one of the allowed options
        if new_category not in self.VALID_CATEGORIES:
            raise ValueError(f"Plant category must be one of {self.VALID_CATEGORIES}.")

        self.__plant_category = new_category

    @property
    def plant_price(self):
        return self.__plant_price

    @plant_price.setter
    def plant_price(self, new_price: float):
        # price must be a positive float, 0 is allowed to represent a free plant
        if new_price < 0:
            raise ValueError("Plant price cannot be negative.")

        self.__plant_price = float(new_price)

    @property
    def stock_level(self):
        return self.__plant_stock_level

    def add_stock(self, amount: int):
        # restocking must add a positive amount
        if amount <= 0:
            raise ValueError("The amount to add must be greater than 0.")

        self.__plant_stock_level += amount

    def stock_level_check_and_buy(self, amount: int):
        if self.stock_level_check(amount):
            self.__plant_stock_level = self.__plant_stock_level - amount
        else:
            raise ValueError("The plant's stock level is not enough.")

    def stock_level_check(self, amount: int) -> bool:
        return self.__plant_stock_level >= amount
