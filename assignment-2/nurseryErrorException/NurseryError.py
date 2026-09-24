class NurseryError(Exception):
    """
    Base Error exception
    """
    def __init__(self, message: str = "A nursery system error occurred.") -> None:
        """
        Create NurseryError object
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """return error message"""
        return self.message
