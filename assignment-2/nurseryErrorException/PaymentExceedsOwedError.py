from nurseryErrorException.NurseryError import NurseryError

class PaymentExceedsOwedError(NurseryError):
    """
    Payment exceeds owed Error exception
    For customer who's trying to over payment the number that they owed
    """
    def __init__(self, message: str = "The payment amount is over the unpaid balance.") -> None:
        """
        Create PaymentExceedsOwedError object
        """
        super().__init__(message)
