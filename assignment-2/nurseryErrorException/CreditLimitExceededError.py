from nurseryErrorException.NurseryError import NurseryError

class CreditLimitExceededError(NurseryError):
    """
    Credit Limit Exceeded Error exception
    For Student/Staff checking their credit limit
    """
    def __init__(self, message: str = "The unpaid balance will exceed $100 for this order") -> None:
        """
        Create CreditLimitExceededError object
        """
        super().__init__(message)
