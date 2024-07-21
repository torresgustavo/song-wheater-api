from domain.shared.errors.base_error import BaseError


class UnexpectedClientError(BaseError):

    def __init__(
        self, client_name: str, error_message: str, detail: dict | None = None
    ):
        self.message = f"Unexpected response from {client_name} - {error_message}"
        self.error_code = "UNEXPECTED_CLIENT_ERROR"
        self.detail = detail

        super().__init__(
            message=self.message, error_code=self.error_code, detail=self.detail
        )
