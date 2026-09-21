class Customer:
    """
    Represents a customer of the nursery and owns all validation of its own
    data (id, name, email, phone number, and duplicate-contact checks).

    Args:
        id (int): unique, positive customer id.
        name (str): customer's name.
        email (str): customer's email address, can be blank if phone_number is given.
        phone_number (str): customer's phone number, can be blank if email is given.

    Attributes:
        __cus_id (int): serial number.
        __cus_name (str): customer's name.
        __cus_email (str): customer's email address.
        __cus_phone_num (str): customer's phone number.
    """

    def __init__(self, id: int, name: str, email: str, phone_number: str):
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

    def __str__(self) -> str:
        """Return a readable, multi-line summary of the customer."""
        cus_id = f'Customer ID: {self.__cus_id}'
        cus_name = f'Customer Name: {self.__cus_name}'
        cus_email = f'Customer Email: {self.__cus_email}'
        cus_phone_number = f'Customer Phone Number: {self.__cus_phone_num}'

        return f"Customer:\n{cus_id}\n{cus_name}\n{cus_email}\n{cus_phone_number}"

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
