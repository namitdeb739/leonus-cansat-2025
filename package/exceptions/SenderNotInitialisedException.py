class SenderNotInitialisedException(BaseException):
    def __init__(self, message: str = "Sender is not initialized.") -> None:
        super().__init__(message)
