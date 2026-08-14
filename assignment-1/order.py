class Order:
    """
    A class for order details

    Args:
        orderId (int)
        cusId (int)
        plantId (int)
        date (str)
        plantPrice (int)
        purchaseAmount (int)
        totalPrice (int)

    Attributes:
        __orderId (int): order's id
        __customerId (int): customer's id
        __plantId (int): plant's id
        __date (str): date of the order placed, format: DD-MM-YYYY
        __purchaseAmount (int): the amount of plants of the order
        __totalPrice (int): the totalPrice of plants
        __status (str): order current status, status: pending/collected/cancelled, default status is pending
    """

    def __init__(self, orderId: int, cusId: int, plantId: int, date: str, plantPrice: int, purchaseAmount: int):
        self.__orderId = orderId
        self.__customerId = cusId
        self.__plantId = plantId
        self.__date = date
        self.__purchaseAmount = purchaseAmount
        self.__totalPrice = self.__totalAmount(plantPrice, purchaseAmount)
        self.__status = 'pending'

    def __str__(self):
        return f"""Order id: {self.__orderId}\nCustomer id: {self.__customerId}\nPlant id: {self.__plantId}\nPruchase amount: {self.__purchaseAmount}\nTotal price: {self.__totalPrice}\nDate: {self.__date}\nStatus: {self.__status}"""

    def __totalAmount(self, plantPrice: int, amount: int):
        totalPrice = amount * plantPrice

        if amount >= 10:
            totalPrice = totalPrice * 0.9
        
        return totalPrice

    @property
    def orderId(self):
        return self.__orderId

    @property
    def customerId(self):
        return self.__customerId

    @property
    def plantId(self):
        return self.__plantId

    @property
    def purchaseAmount(self):
        return self.__purchaseAmount

    @property
    def status(self):
        return self.__status

    @property
    def cancelCheck(self):
        if self.__status == 'pending':
            return True
        else:
            return False

    @status.setter
    def status(self, newStatus):
        statusAry = ['pending', 'collected', 'cancelled']

        # verify valid status
        if newStatus not in statusAry:
            raise ValueError("Please enter valid status")

        # changing into new status
        self.__status = newStatus