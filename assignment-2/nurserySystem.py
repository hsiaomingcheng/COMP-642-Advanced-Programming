from order import Order
from plant import Plant
from customer import Customer
from datetime import date

class NurserySystem:
    """
    This is the central of the whole system.
    User can create new custome, plant, order through this class.
    Also, for the searching and listing.
    """

    def __init__(self):
        self.__customers = []
        self.__plants = []
        self.__orders = []

    def addCustomer(self, newCus: Customer):
        # blank email/phone number is already rejected by Customer's own constructor

        # verify customer ID is unique within the system
        if self.customerInfo(newCus.id):
            raise ValueError("This customer ID already exists")

        # reject the request if the email or phone number is already used by
        # an existing customer; Customer owns this comparison logic
        for cus in self.__customers:
            if cus.conflicts_with(newCus):
                raise ValueError("The email or phone number has already been used.")

        # add new customer
        self.__customers.append(newCus)

    def customerInfo(self, cusId):
        for cus in self.__customers:
            if cus.id == cusId:
                return cus
        return None

    def addPlant(self, newPlant: Plant):
        # verify plant ID
        if self.plantInfo(newPlant.id):
            raise ValueError("This plant ID already exists")

        # add new plant
        self.__plants.append(newPlant)

    def plantInfo(self, plantId: int):
        for plant in self.__plants:
            if plant.id == plantId:
                return plant
        return None

    def availablePlantList(self):
        # only show plants that currently have stock available
        availablePlants = [plant for plant in self.__plants if plant.stock_level_check(1)]

        for index, plant in enumerate(availablePlants):
            if index != 0:
                print("---")
            print(plant)


    def placeOrder(self, customerId: int, plantId: int, amount: int):
        targetCustomer = None
        targetPlant = None

        # if the user trying to place a order with 0 amount, then reject.
        if amount <= 0:
            raise ValueError("The amount need to be greatter than 0.")

        # verify if it is a valid customer
        for cus in self.__customers:
            if cus.id == customerId:
                targetCustomer = cus

        # verify if it is a valid plant
        for plant in self.__plants:
            if plant.id == plantId:
                targetPlant = plant

        # block the process if user enter invalid customer and plant id
        if targetCustomer is None or targetPlant is None:
            raise ValueError("Please enter a valid customer and plant.")

        # Check the stock level, and reduce stock level if it is enough
        targetPlant.stock_level_check_and_buy(amount)

        # making an order
        self.__orders.append(
            Order(
                len(self.__orders) + 1,
                targetCustomer,
                targetPlant,
                date.today().strftime("%d-%m-%Y"),
                amount
            )
        )

    def cancelOrder(self, orderId: int):
        """
        Cancel a pending order. The Order itself validates that it is still
        pending and returns the purchased stock to its plant.
        """
        # get order info
        targetOrder = self.orderInfo(orderId)

        # showing error message when it is a invalid order id
        if targetOrder is None:
            raise ValueError("Please enter valid order Id")

        targetOrder.cancel()

    def collectOrder(self, orderId: int):
        """
        Mark a pending order as collected. The Order itself validates that it
        is not cancelled or already collected.
        """
        targetOrder = self.orderInfo(orderId)

        if targetOrder is None:
            raise ValueError("Please enter valid order Id")

        targetOrder.collect()

    def orderInfo(self, orderId: int):
        for o in self.__orders:
            if o.order_id == orderId:
                return o
        return None

    def checkOrderStatus(self, orderId: int) -> str:
        targetOrder = self.orderInfo(orderId)

        if targetOrder is None:
            raise ValueError("Please enter valid order Id")

        return targetOrder.status

    def customerOrderHistory(self, cusId: int):
        length = 0

        # verify the customer
        targetCustomer = self.customerInfo(cusId)
        if targetCustomer is None:
            raise ValueError("Please enter an exsit customer ID.")

        # print the details of order of the specific customer
        for order in self.__orders:
            if order.customer_id == cusId:
                if length != 0:
                    print("---")

                length += 1
                print(order)

        print("")
        print(f"The customer has total {length} orders.")


    def customerList(self):
        for index, cus in enumerate(self.__customers):
            if index != 0:
                print("---")
            print(cus)

    def plantList(self):
        for index, plant in enumerate(self.__plants):
            if index != 0:
                print("---")
            print(plant)

    def orderList(self):
        for index, order in enumerate(self.__orders):
            if index != 0:
                print("---")
            print(order)