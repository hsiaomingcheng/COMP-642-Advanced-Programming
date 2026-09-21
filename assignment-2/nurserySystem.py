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

    def add_customer(self, new_cus: Customer):
        # blank email/phone number is already rejected by Customer's own constructor

        # verify customer ID is unique within the system
        if self.customer_info(new_cus.id):
            raise ValueError("This customer ID already exists")

        # reject the request if the email or phone number is already used by
        # an existing customer; Customer owns this comparison logic
        for cus in self.__customers:
            if cus.conflicts_with(new_cus):
                raise ValueError("The email or phone number has already been used.")

        # add new customer
        self.__customers.append(new_cus)

    def customer_info(self, cus_id):
        for cus in self.__customers:
            if cus.id == cus_id:
                return cus
        return None

    def add_plant(self, new_plant: Plant):
        # verify plant ID
        if self.plant_info(new_plant.id):
            raise ValueError("This plant ID already exists")

        # add new plant
        self.__plants.append(new_plant)

    def plant_info(self, plant_id: int):
        for plant in self.__plants:
            if plant.id == plant_id:
                return plant
        return None

    def available_plant_list(self):
        # only show plants that currently have stock available
        available_plants = [plant for plant in self.__plants if plant.stock_level_check(1)]

        for index, plant in enumerate(available_plants):
            if index != 0:
                print("---")
            print(plant)

    def place_order(self, customer_id: int, plant_id: int, amount: int):
        target_customer = None
        target_plant = None

        # if the user trying to place a order with 0 amount, then reject.
        if amount <= 0:
            raise ValueError("The amount need to be greatter than 0.")

        # verify if it is a valid customer
        for cus in self.__customers:
            if cus.id == customer_id:
                target_customer = cus

        # verify if it is a valid plant
        for plant in self.__plants:
            if plant.id == plant_id:
                target_plant = plant

        # block the process if user enter invalid customer and plant id
        if target_customer is None or target_plant is None:
            raise ValueError("Please enter a valid customer and plant.")

        # Check the stock level, and reduce stock level if it is enough
        target_plant.stock_level_check_and_buy(amount)

        # making an order
        self.__orders.append(
            Order(
                len(self.__orders) + 1,
                target_customer,
                target_plant,
                date.today().strftime("%d-%m-%Y"),
                amount
            )
        )

    def cancel_order(self, order_id: int):
        """
        Cancel a pending order. The Order itself validates that it is still
        pending and returns the purchased stock to its plant.
        """
        # get order info
        target_order = self.order_info(order_id)

        # showing error message when it is a invalid order id
        if target_order is None:
            raise ValueError("Please enter valid order Id")

        target_order.cancel()

    def collect_order(self, order_id: int):
        """
        Mark a pending order as collected. The Order itself validates that it
        is not cancelled or already collected.
        """
        target_order = self.order_info(order_id)

        if target_order is None:
            raise ValueError("Please enter valid order Id")

        target_order.collect()

    def order_info(self, order_id: int):
        for o in self.__orders:
            if o.order_id == order_id:
                return o
        return None

    def check_order_status(self, order_id: int) -> str:
        target_order = self.order_info(order_id)

        if target_order is None:
            raise ValueError("Please enter valid order Id")

        return target_order.status

    def customer_order_history(self, cus_id: int):
        length = 0

        # verify the customer
        target_customer = self.customer_info(cus_id)
        if target_customer is None:
            raise ValueError("Please enter an exsit customer ID.")

        # print the details of order of the specific customer
        for order in self.__orders:
            if order.customer_id == cus_id:
                if length != 0:
                    print("---")

                length += 1
                print(order)

        print("")
        print(f"The customer has total {length} orders.")

    def customer_list(self):
        for index, cus in enumerate(self.__customers):
            if index != 0:
                print("---")
            print(cus)

    def plant_list(self):
        for index, plant in enumerate(self.__plants):
            if index != 0:
                print("---")
            print(plant)

    def order_list(self):
        for index, order in enumerate(self.__orders):
            if index != 0:
                print("---")
            print(order)
