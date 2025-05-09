from fastapi import HTTPException, status


class CurrencyAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="There is already a currency with the same code.")


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")


class OnlyAdminException(HTTPException):
    def __init__(self, action) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=f"Only administrators can {action}.")
