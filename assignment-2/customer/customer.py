from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order.order import Order

class Customer(ABC):
    """
    Represents a customer of the nursery and owns all validation of its own
    data (id, name, email, phone number, and duplicate-contact checks).

    Args:
        id (int): unique, positive customer id.
        name (str): customer's name.
        email (str): customer's email address, can be blank if phone_number is given.
        phone_number (str): customer's phone number, can be blank if email is given.
        balance (float): customer's unpaid balance, starting from 0.

    Attributes:
        __cus_id (int): serial number.
        __cus_name (str): customer's name.
        __cus_email (str): customer's email address.
        __cus_phone_num (str): customer's phone number.
        __cus_balance (float): customer's unpaid balance.
        __cus_order(list): customer's orders.
    """

    # limit amount of Staff/Student
    CREDIT_LIMIT = 100

    def __init__(self, id: int, name: str, email: str, phone_number: str, balance: float = 0) -> None:
        # id must be a positive integer
        if not isinstance(id, int) or id <= 0:
            raise ValueError("Customer id must be a positive integer.")

        # name must not be blank
        if not name:
            raise ValueError("Customer name cannot be blank.")

        # at least one contact method is required
        if not email and not phone_number:
            raise ValueError("You need to enter at least email or phone number.")

        self.__cus_id = id
        self.__cus_name = name
        self.__cus_email = email
        self.__cus_phone_num = phone_number
        self.__cus_balance = balance
        self.__cus_order = []

    def __str__(self) -> str:
        """Return a readable, multi-line summary of the customer."""
        cus_id = f'Customer ID: {self.__cus_id}'
        cus_name = f'Customer Name: {self.__cus_name}'
        cus_email = f'Customer Email: {self.__cus_email}'
        cus_phone_number = f'Customer Phone Number: {self.__cus_phone_num}'
        cus_balance = f'Customer Unpaid Balance: {self.__cus_balance}'
        cus_type = f'Customer Type: {self.customer_type}'

        return f"Customer:\n{cus_id}\n{cus_name}\n{cus_email}\n{cus_phone_number}\n{cus_balance}\n{cus_type}"

    @property
    def id(self) -> int:
        """int: the customer's id."""
        return self.__cus_id

    @property
    def name(self) -> str:
        """str: the customer's name."""
        return self.__cus_name

    @property
    def email(self) -> str:
        """str: the customer's email address."""
        return self.__cus_email

    @property
    def phone_number(self) -> str:
        """str: the customer's phone number."""
        return self.__cus_phone_num

    @property
    def balance(self) -> float:
        """float: the customer's unpaid balance."""
        return self.__cus_balance

    @property
    def orders(self) -> list:
        """list: customer's order list."""
        return self.__cus_order

    @property
    @abstractmethod
    def customer_type(self) -> str:
        """str: return the type of customer(Staff/Student/Community)"""
        pass

    @property
    def discount_rate(self) -> float:
        """float: return the default discount rate for customer"""
        return 0.0

    def conflicts_with(self, other: "Customer") -> bool:
        """
        Check whether this customer shares an email or phone number with
        another customer, which should not be allowed within the system.

        Args:
            other (Customer): the customer to compare against.

        Returns:
            bool: True if the email or phone number is already used by other.
        """
        same_email = bool(self.__cus_email) and self.__cus_email == other.email
        same_phone = bool(self.__cus_phone_num) and self.__cus_phone_num == other.phone_number

        return same_email or same_phone

    def add_to_balance(self, order_total_amount: float) -> None:
        """Combining customer's order total amount and its unpaid balance when placing an order."""
        self.__cus_balance += order_total_amount

    def reduce_balance(self, amount: float) -> None:
        """Minus customer's unpaid balance, and verify the recuding amount."""
        if amount > self.__cus_balance:
            raise ValueError("The reducing amount cannot greater than the customer unpaid balance.")

        self.__cus_balance = self.__cus_balance - amount

    def record_order(self, order: "Order") -> None:
        """Adding a new order into customer's order list"""
        self.__cus_order.append(order)

    def check_can_place_order(self, prospective_total: float) -> None:
        """Verify the customer balance to prevent it over 100 dollars."""
        if self.__cus_balance + prospective_total > self.CREDIT_LIMIT:
            raise ValueError("The unpaid balance is going to over $100.")
