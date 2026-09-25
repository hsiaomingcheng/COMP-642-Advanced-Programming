import os, pickle, atexit
from order.order import Order
from plant.plant import Plant
from customer.customer import Customer
from payment.payment import Payment
from datetime import date

class NurserySystem:
    """
    This is the central of the whole system.
    User can create new custome, plant, order through this class.
    Also, for the searching and listing.
    """

    def __init__(self, file: str) -> None:
        self.__customers = []
        self.__plants = []
        self.__orders = []
        self.__payments = []
        self.__file = os.path.join(os.path.dirname(__file__), file)

        self.load()
        atexit.register(self.save)

    def save(self) -> None:
        """save customers, plants, orders, payments together as a pickle file"""
        system_contents = (self.__customers, self.__plants, self.__orders, self.__payments)
        with open(self.__file, "wb") as f:
            pickle.dump(system_contents, f)

    def load(self) -> None:
        """
        load the pickle file and give the value back to
        the self.__customer,self.__plants, self.__orders, self.__payments
        """

        # if file exist then load the file otherwise programme will crash
        # due to the atexit.register(self.save) in init at the beginning
        if os.path.exists(self.__file):
            try:
                with open(self.__file, "rb") as f:
                    customers, plants, orders, payments = pickle.load(f)
                    
                    self.__customers = customers
                    self.__plants = plants
                    self.__orders = orders
                    self.__payments = payments
            except Exception:
                print("Failed to load the file.")

    def add_customer(self, new_cus: Customer) -> None:
        """
        Add a new customer to the system.

        Args:
            new_cus (Customer): the customer to add.

        Raises:
            ValueError: if the customer's id already exists, or its email/phone
                number is already used by an existing customer.
        """
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

    def customer_info(self, cus_id: int) -> Customer | None:
        """Return the customer with the given id, or None if not found."""
        # linear search, there's no index by id
        for cus in self.__customers:
            if cus.id == cus_id:
                return cus
        return None

    def add_plant(self, new_plant: Plant) -> None:
        """
        Add a new plant to the system.

        Args:
            new_plant (Plant): the plant to add.

        Raises:
            ValueError: if the plant's id already exists.
        """
        # verify plant ID
        if self.plant_info(new_plant.id):
            raise ValueError("This plant ID already exists")

        # add new plant
        self.__plants.append(new_plant)

    def plant_info(self, plant_id: int) -> Plant | None:
        """Return the plant with the given id, or None if not found."""
        # linear search, there's no index by id
        for plant in self.__plants:
            if plant.id == plant_id:
                return plant
        return None

    def available_plant_list(self) -> None:
        """Print every plant that currently has at least 1 unit in stock."""
        # only show plants that currently have stock available
        available_plants = [plant for plant in self.__plants if plant.stock_level_check(1)]

        for index, plant in enumerate(available_plants):
            if index != 0:
                print("---")
            print(plant)

    def place_order(self, customer_id: int, item_list: list[tuple[int, int]]) -> int:
        """
        Place a new order for a customer and plant, reducing the plant's stock.
        """
        target_customer = self.customer_info(customer_id)

        # block the process if user enter invalid customer
        if target_customer is None:
            raise ValueError("Please enter a valid customer.")

        # create a new order object right here
        new_order = Order(
            len(self.__orders) + 1,
            target_customer,
            date.today().strftime("%d-%m-%Y")
        )

        # Trying to find each plant from the item_list and add item record for the order
        for plant_id, quantity in item_list:
            plant = self.plant_info(plant_id)
            if plant is None:
                raise ValueError(f"The plant, ID: {plant_id}, was not found.")
            
            new_order.add_item(plant, quantity)

        # place a new order
        new_order.place()

        # making an order
        self.__orders.append(new_order)

        return new_order.order_id

    def cancel_order(self, order_id: int) -> None:
        """
        Cancel a pending order. The Order itself validates that it is still
        pending and returns the purchased stock to its plant.

        Raises:
            ValueError: if order_id does not exist, or the order is not pending.
        """
        # get order info
        target_order = self.order_info(order_id)

        # showing error message when it is a invalid order id
        if target_order is None:
            raise ValueError("Please enter valid order Id")

        target_order.cancel()

    def collect_order(self, order_id: int) -> None:
        """
        Mark a pending order as collected. The Order itself validates that it
        is not cancelled or already collected.

        Raises:
            ValueError: if order_id does not exist, or the order cannot be
                collected (already cancelled or already collected).
        """
        target_order = self.order_info(order_id)

        if target_order is None:
            raise ValueError("Please enter valid order Id")

        target_order.collect()

    def order_info(self, order_id: int) -> Order | None:
        """Return the order with the given id, or None if not found."""
        # linear search, there's no index by id
        for o in self.__orders:
            if o.order_id == order_id:
                return o
        return None

    def check_order_status(self, order_id: int) -> str:
        """
        Return the current status of an order.

        Raises:
            ValueError: if order_id does not exist.
        """
        target_order = self.order_info(order_id)

        if target_order is None:
            raise ValueError("Please enter valid order Id")

        return target_order.status

    def customer_order_history(self, cus_id: int) -> None:
        """
        Print every order (including cancelled ones) placed by a customer.

        Raises:
            ValueError: if cus_id does not exist.
        """
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

    def customer_list(self) -> None:
        """Print every customer in the system."""
        # print a '---' separator between entries, but not before the first one
        for index, cus in enumerate(self.__customers):
            if index != 0:
                print("---")
            print(cus)

    def plant_list(self) -> None:
        """Print every plant in the system."""
        for index, plant in enumerate(self.__plants):
            if index != 0:
                print("---")
            print(plant)

    def order_list(self) -> None:
        """Print every order in the system."""
        for index, order in enumerate(self.__orders):
            if index != 0:
                print("---")
            print(order)

    def make_payment(self, payment: "Payment") -> None:
        # checking if the payment id is already exsisted.
        # if is exsisted, means this payment is already paid.
        for item in self.__payments:
            if item.payment_id == payment.payment_id:
                raise ValueError("The payment id is already exsisted.")

        # verify this is a real order
        is_real_order = self.order_info(payment.order.order_id)

        if is_real_order is None:
            raise ValueError("The order is not exsisted.")

        # verify is the same person who make the payment and the order
        if payment.customer.id != payment.order.customer_id:
            raise ValueError("Customer need to be the same one of the payment and order.")

        # check the status of order to determine if this is a acceptable payment
        payment.order.check_can_accept_payment(payment)

        # record the payment
        payment.order.record_payment(payment)

        # reduce the balance of the customer
        payment.customer.reduce_balance(payment.amount)

        # put this payment into system payment list(self.__payments)
        self.__payments.append(payment)