from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer.customer import Customer
    from order.order import Order

class Payment(ABC):
    """
    Payment class is a record for each payment
    """
    def __init__(self, payment_id: int, amount: float, customer: "Customer", order: "Order", date: str) -> None:
        """
        create init data for the object
        """

        # id must be a positive integer
        if not isinstance(payment_id, int) or payment_id <= 0:
            raise ValueError("Payment id must be a positive integer.")

        # verify amount
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        # date must be in DD-MM-YYYY format
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Payment date must be in DD-MM-YYYY format.")

        self.__payment_id = payment_id
        self.__amount = amount
        self.__customer = customer
        self.__order = order
        self.__date = date

    def __str__(self) -> str:
        """Return a readable, multi-line summary of the payment."""
        return (
            f"Payment:\n"
            f"Payment amount: {self.__amount}\n"
            f"Customer: {self.__customer.name} (id: {self.__customer.id})\n"
            f"Order id: {self.__order.order_id}\n"
            f"Date: {self.__date}\n"
            f"Payment Type: {self.payment_type}\n"
            f"Surcharge: {self.surcharge}\n"
            f"Total charge: {self.get_total_charged()}\n"
        )

    @property
    def payment_id(self) -> int:
        """return id of the payment"""
        return self.__payment_id

    @property
    def amount(self) -> float:
        """return amount of the payment"""
        return self.__amount

    @property
    def customer(self) -> "Customer":
        """return customer of the payment"""
        return self.__customer

    @property
    def order(self) -> "Order":
        """return order of the payment"""
        return self.__order

    @property
    def date(self) -> str:
        """return date of the payment"""
        return self.__date

    @property
    @abstractmethod
    def payment_type(self) -> str:
        """base method of payment type"""
        pass

    @property
    def surcharge(self) -> float:
        """return surcharge fee"""
        return 0.0

    def get_total_charged(self) -> float:
        """return the total charge of the customer"""
        return round(self.__amount + self.surcharge, 2)

    def verify_card_number(self, card_number) -> None:
        for letter in card_number:
            if not letter.isdecimal():
                raise ValueError("The card number needs to be a 16-digit length integer.")

        if len(card_number) != 16:
            raise ValueError("The card number needs to be a 16-digit length integer.")
