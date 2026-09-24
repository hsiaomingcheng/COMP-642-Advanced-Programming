from nurseryErrorException.NurseryError import NurseryError

class InsufficientStockError(NurseryError):
    """
    Insufficient Stock Error exception
    """
    def __init__(self, message: str = "The stock is insufficient") -> None:
        """
        Create InsufficientStockError object
        """
        super().__init__(message)
