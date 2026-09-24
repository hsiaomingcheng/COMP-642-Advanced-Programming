from nurseryErrorException.NurseryError import NurseryError

class PendingOrderExistsError(NurseryError):
    """
    Pending order exists Error exception
    For community customer
    if they trying to order a second order while they have't collected their first order
    """
    def __init__(self, message: str = "The previous order has not been colleced yet.") -> None:
        """
        Create PendingOrderExistsError object
        """
        super().__init__(message)
