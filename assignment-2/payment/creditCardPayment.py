from payment.payment import Payment
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer.customer import Customer
    from order.order import Order

class CreditCardPayment(Payment):
    """
    child class of Payment class, for credit card
    """
    SURCHARGE_RATE = 0.015

    def __init__(
            self,
            payment_id: int,
            amount: float,
            customer: "Customer",
            order: "Order",
            date: str,
            card_number: str,
            expiry_date: str
        ) -> None:
        """init CreditCardPayment attributes"""

        # verify card number
        self.verify_card_number(card_number)

        # date must be in MM/YY format
        try:
            datetime.strptime(expiry_date, "%m/%y")
        except ValueError:
            raise ValueError("The card's expiry date format is incorrect.")

        super().__init__(payment_id, amount, customer, order, date)
        self.__card_number = card_number
        self.__expiry_date = expiry_date

    def __str__(self) -> str:
        return (
            super().__str__()+
            f"Card Number: {self.__card_number}\n"
            f"Expiry Date: {self.__expiry_date}"
        )

    @property
    def payment_type(self) -> str:
        """return payment type"""
        return "Credit Card"

    @property
    def surcharge(self) -> float:
        """return surcharge fee"""
        return round(self.amount * self.SURCHARGE_RATE, 2)

    @property
    def card_number(self) -> str:
        """return card number"""
        return self.__card_number

    @property
    def expiry_date(self) -> str:
        """return expiry date"""
        return self.__expiry_date
