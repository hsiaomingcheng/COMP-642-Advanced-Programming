from datetime import datetime

from customer import Customer
from plant import Plant


class Order:
    """
    A class for order details

    Args:
        order_id (int)
        customer (Customer): the customer object this order belongs to
        plant (Plant): the plant object this order is for
        date (str)
        purchase_amount (int)

    Attributes:
        __order_id (int): order's id
        __customer (Customer): the customer object this order belongs to
        __plant (Plant): the plant object this order is for
        __date (str): date of the order placed, format: DD-MM-YYYY
        __purchase_amount (int): the amount of plants of the order
        __total_price (float): the total price of the order
        __status (str): order current status, status: pending/collected/cancelled, default status is pending
    """

    def __init__(self, order_id: int, customer: Customer, plant: Plant, date: str, purchase_amount: int):
        # date must be in DD-MM-YYYY format
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Order date must be in DD-MM-YYYY format.")

        self.__order_id = order_id
        self.__customer = customer
        self.__plant = plant
        self.__date = date
        self.__purchase_amount = purchase_amount
        self.__total_price = self.__total_amount(plant.plant_price, purchase_amount)
        self.__status = 'pending'

    def __str__(self):
        return f"""Order:\nOrder id: {self.__order_id}\nCustomer: {self.__customer.name} (id: {self.__customer.id})\nPlant: {self.__plant.name} (id: {self.__plant.id})\nPruchase amount: {self.__purchase_amount}\nTotal price: {self.__total_price}\nDate: {self.__date}\nStatus: {self.__status}"""

    def __total_amount(self, plant_price: float, amount: int):
        total_price = amount * plant_price

        if amount >= 10:
            total_price = total_price * 0.9

        return total_price

    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer(self):
        return self.__customer

    @property
    def plant(self):
        return self.__plant

    @property
    def customer_id(self):
        return self.__customer.id

    @property
    def plant_id(self):
        return self.__plant.id

    @property
    def date(self):
        return self.__date

    @property
    def purchase_amount(self):
        return self.__purchase_amount

    @property
    def status(self):
        return self.__status

    def cancel(self):
        # only a pending order can be cancelled
        if self.__status != 'pending':
            raise ValueError("A collected or cancelled order cannot be cancelled.")

        self.__status = 'cancelled'

        # give the stock back to the plant
        self.__plant.add_stock(self.__purchase_amount)

    def collect(self):
        # a cancelled order can never be collected
        if self.__status == 'cancelled':
            raise ValueError("A cancelled order cannot be collected.")

        # a collected order cannot be collected again or moved back to pending
        if self.__status == 'collected':
            raise ValueError("This order has already been collected.")

        self.__status = 'collected'
