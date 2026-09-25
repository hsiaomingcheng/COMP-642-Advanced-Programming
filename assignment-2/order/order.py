from datetime import datetime
from plant.plant import Plant
from order.orderItem import OrderItem
from nurseryErrorException.InsufficientStockError import InsufficientStockError
from nurseryErrorException.PaymentExceedsOwedError import PaymentExceedsOwedError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer.customer import Customer
    from payment.payment import Payment

class Order:
    """
    A class for order details

    Args:
        order_id (int)
        customer (Customer): the customer object this order belongs to
        date (str)

    Attributes:
        __order_id (int): order's id
        __customer (Customer): the customer object this order belongs to
        __date (str): date of the order placed, format: DD-MM-YYYY
        __status (str): order current status, status: pending/collected/cancelled, default status is pending
    """

    def __init__(self, order_id: int, customer: "Customer", date: str) -> None:
        """
        Create an order, documenting order id, customer object, data, status, order items, and payments 

        Raises:
            ValueError: if date is not in DD-MM-YYYY format.
        """
        # date must be in DD-MM-YYYY format
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Order date must be in DD-MM-YYYY format.")

        self.__order_id = order_id
        self.__customer = customer
        self.__date = date
        self.__status = 'pending'
        self.__items = []
        self.__payments = []

    def __str__(self) -> str:
        """Return a readable, multi-line summary of the order."""
        return (
            f"Order:\n"
            f"Order id: {self.__order_id}\n"
            f"Customer: {self.__customer.name} (id: {self.__customer.id})\n"
            f"Date: {self.__date}\n"
            f"Status: {self.__status}\n"
            f"Paid: {self.get_amount_paid()}\n"
            f"Owed: {self.get_amount_owed()}"
        )

    @property
    def order_id(self) -> int:
        """int: the order's id."""
        return self.__order_id

    @property
    def customer(self) -> "Customer":
        """Customer: the customer this order belongs to."""
        return self.__customer

    @property
    def customer_id(self) -> int:
        """int: id of the customer this order belongs to."""
        return self.__customer.id

    @property
    def date(self) -> str:
        """str: the date the order was placed, in DD-MM-YYYY format."""
        return self.__date

    @property
    def status(self) -> str:
        """str: the order's current status ('pending', 'collected', or 'cancelled')."""
        return self.__status

    @property
    def order_items(self) -> list:
        """return order item list"""
        return list(self.__items)

    @property
    def order_payments(self) -> list:
        """return order payment list"""
        return list(self.__payments)

    def add_item(self, plant: "Plant", quantity: int) -> None:
        """
        if the order status is not pending, then it cannot be added new item
        if the item is already existed, then add quantity to the item directly.
        if cannot find any existed item,
        then create a new OrderItem object and put into the __items list.
        """
        if self.__status != "pending":
            raise ValueError("Only pending order can change quantity.")

        for item in self.__items:
            if item.plant.id == plant.id:
                item.add_quantity(quantity)
                return

        self.__items.append(OrderItem(plant, quantity))
                  
    def get_subtotal(self) -> float:
        """caculate the total cost of each item"""
        subtotal = 0

        for item in self.__items:
            subtotal += round(item.get_cost(), 2)

        return subtotal

    def get_total(self) -> float:
        """return the total amount of all items that times their own discount rate"""
        subtotal = self.get_subtotal()

        return round(subtotal * (1 - self.__customer.discount_rate), 2)

    def get_amount_paid(self) -> float:
        """Check how much already paid for this order"""
        amount = 0.0
        for payment in self.__payments:
            amount += payment.amount
            
        return round(amount, 2)

    def get_amount_owed(self) -> float:
        """Check how much still owed for this order"""
        if self.status == "cancelled":
            return 0.0

        return round(self.get_total() - self.get_amount_paid(), 2)

    def is_fully_paid(self) -> bool:
        """return true if there's no money left to pay"""
        return self.get_amount_owed() == 0

    def check_can_accept_payment(self, payment: "Payment") -> None:
        """
        If the order not owed any money or has been cancelled
        If the payment amount is not greater than owed amount

        If these two verify were not triggered, it means that was a acceptable payment.
        """
        if self.is_fully_paid() or self.__status == "cancelled":
            raise PaymentExceedsOwedError("The order has already cancelled or fully paid.")

        if payment.amount > self.get_amount_owed():
            raise PaymentExceedsOwedError("The payment amount exceeds the owed amount.")

    def record_payment(self, payment: "Payment") -> None:
        """put payment into payments list as a payment record"""
        self.__payments.append(payment)

    def place(self) -> None:
        """
        if any of these verify down there goes wrong the programme will stop here,
        and nothing happen except showing the error message

        The whole idea is the customer need the pass the verify of their credit limit,
        or no current pending order depending on their customer type.
        Then, check the stock, if all the plant stock are enough for
        each items' requirement, then reduce the stock
        """
        if len(self.__items) == 0:
            raise ValueError("Cannot find any item in the order.")

        total_amount_of_payment = self.get_total()

        # Verify the customer balance
        self.__customer.check_can_place_order(total_amount_of_payment)

        for item in self.__items:
            # Verify the stock level of every item, making the stock level is enough for purchase
            if not item.check_stock():
                raise InsufficientStockError(
                    f"Sorry, the stock level of {item.plant.name} is not enough."
                )

        for item in self.__items:
            # Reducing the stock number of each item
            item.reserve_stock()

        # Adding the total balance and order record for the specific customer
        self.__customer.add_to_balance(total_amount_of_payment)
        self.__customer.record_order(self)

    def cancel(self) -> None:
        """
        order status can only be cancelled when its status is pending

        the process of cancel
        1. return each item stock
        2. remove the balance amount of the customer
        3. set the order status to 'cancelled'
        """
        if len(self.__payments) > 0:
            raise ValueError("Paid/Partially-paid order cannot be cancelled.")

        if self.__status != "pending":
            raise ValueError("The order status needs to be 'Pending' to cancel it.")

        for item in self.__items:
            item.return_stock()

        self.__customer.reduce_balance(self.get_total())

        self.__status = "cancelled"

    def collect(self) -> None:
        """
        order status can only be collected when its status is pending

        calling check_can_collect to see if the customer meet the collection requirement
        """
        if self.__status != "pending":
            raise ValueError("The order status needs to be 'Pending' to collect it.")

        self.__customer.check_can_collect(self)

        self.__status = "collected"


