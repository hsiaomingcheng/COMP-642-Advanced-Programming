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
        # reject the request, if email and phoneNumber is blank
        if newCus.email == "" and newCus.phoneNumber == "":
            raise ValueError("You need to enter at least email or phone number.")

        # verify if the new customer's email and phone number is already exist
        # if it is already exist, then reject the request
        for cus in self.__customers:
            if newCus.email != "" and cus.email == newCus.email:
                raise ValueError("The email has already been used.")

            if newCus.phoneNumber != "" and cus.phoneNumber == newCus.phoneNumber:
                raise ValueError("The phone number has already been used.")

        # add new customer
        self.__customers.append(newCus)

    def customerInfo(self, cusId):
        for cus in self.__customers:
            if cus.id == cusId:
                return cus


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


    def placeOrder(self, customerId: int, plantId: int, amount: int):
        isValidCustomer = False
        isValidPlant = False
        targetPlant = None

        # if the user trying to place a order with 0 amount, then reject.
        if amount <= 0:
            raise ValueError("The amount need to be greatter than 0.")

        # verify if it is a valid customer
        for cus in self.__customers:
            if cus.id == customerId:
                isValidCustomer = True

        # verify if it is a valid plant
        for plant in self.__plants:
            if plant.id == plantId:
                isValidPlant = True
                targetPlant = plant

        # block the process if user enter invalid customer and plant id
        if not isValidCustomer or not isValidPlant:
            raise ValueError("Please enter a valid customer and plant.")

        # Check the stock level, and reduce stock level if it is enough
        targetPlant.stockLevelCheckAndBuy(amount)

        # making an order
        self.__orders.append(
            Order(
                len(self.__orders) + 1,
                customerId,
                plantId,
                date.today().strftime("%d-%m-%Y"),
                targetPlant.plantPrice,
                amount
            )
        )

    def cancelOrder(self, orderId: int):
        """
        cancel a order need to do two things

        1. change order status into 'cancelled', if the status is 'collected', then it cannot be cancelled
        2. adding the stock back to the plant, if it got cancelled successfully
        """
        # get order info
        targetOrder = self.orderInfo(orderId)

        # showing error message when it is a invalid order id
        if targetOrder is None:
            raise ValueError("Please enter valid order Id")

        # verify the status before cancel
        if not targetOrder.cancelCheck:
            raise ValueError("A collected or cancelled order cannot cancel")

        # change order status
        targetOrder.status = 'cancelled'

        # adding stock back to the plant object
        for plant in self.__plants:
            if plant.id == targetOrder.plantId:
                plant.stockLevel = targetOrder.purchaseAmount

    def orderInfo(self, orderId: int):
        # finding the order
        for o in self.__orders:
            if o.orderId == orderId:
                return o

        return None

    def updateOrderStatus(self, orderId: int, status: str):
        """
        First, stop any cancel status with out using cancelOrder method
        Second, reject invalid order id
        Thrid, a cancelled order cannot change its status again
        """
        # prevent user skip cancelCheck to set cancelled status
        if status == 'cancelled':
            raise ValueError("Please use cancelOrder to cancel an order.")

        targetOrder = self.orderInfo(orderId)

        # verify the order
        if targetOrder is None:
            raise ValueError("Please enter an exist order ID.")

        # cancelled order is not allow to be changed its status
        if targetOrder.status == 'cancelled':
            raise ValueError("Cancelled order cannot change order status")

        targetOrder.status = status

    def customerOrderHistory(self, cusId: int):
        length = 0

        # verify the customer
        targetCustomer = self.customerInfo(cusId)
        if targetCustomer is None:
            raise ValueError("Please enter an exsit customer ID.")

        # print the details of order of the specific customer
        for order in self.__orders:
            if order.customerId == cusId:
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