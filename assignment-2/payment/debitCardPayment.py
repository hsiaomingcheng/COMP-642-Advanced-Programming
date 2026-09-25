from payment.payment import Payment
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer.customer import Customer
    from order.order import Order

class DebitCardPayment(Payment):
    """
    child class of Payment class, for debit card
    """
    def __init__(
            self,
            payment_id: int,
            amount: float,
            customer: "Customer",
            order: "Order",
            date: str,
            card_number: str,
            bank_name: str
        ) -> None:
        """init DebitCardPayment attributes"""

        # verify card number
        self.verify_card_number(card_number)

        if not bank_name.strip():
            raise ValueError("Bank name cannot be a blank.")

        super().__init__(payment_id, amount, customer, order, date)
        self.__card_number = card_number
        self.__bank_name = bank_name

    def __str__(self) -> str:
        return (
            super().__str__()+
            f"Card Number: {self.__card_number}\n"
            f"Bank Name: {self.__bank_name}"
        )

    @property
    def payment_type(self) -> str:
        """return payment type"""
        return "Debit Card"

    @property
    def card_number(self) -> str:
        """return card number"""
        return self.__card_number

    @property
    def bank_name(self) -> str:
        """return bank name"""
        return self.__bank_name
