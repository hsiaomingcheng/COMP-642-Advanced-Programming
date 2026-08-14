class Customer:
    """
    A class for document all the details of customers

    Args:
        id (int)
        name (str)
        email (str)
        phoneNumber (str)

    Attributes:
        __cusId (int): serial number
        __cusName (str): customer's name
        __cusEmail (str): customer's email address
        __cusPhoneNum (str): customer's phone number
    """

    def __init__(self, id: int, name: str, email: str, phoneNumber: str):
        self.__cusId = id
        self.__cusName = name
        self.__cusEmail = email
        self.__cusPhoneNum = phoneNumber

    def __str__(self):
        cusId = f'Customer ID: {self.__cusId}'
        cusName = f'Customer Name: {self.__cusName}'
        cusEmail = f'Customer Email: {self.__cusEmail}'
        cusPhoneNumber = f'Customer Phone Number: {self.__cusPhoneNum}'

        return f"{cusId}\n{cusName}\n{cusEmail}\n{cusPhoneNumber}"

    @property
    def id(self):
        return self.__cusId

    @property
    def email(self):
        return self.__cusEmail

    @property
    def phoneNumber(self):
        return self.__cusPhoneNum
