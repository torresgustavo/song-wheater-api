from domain.shared.errors.base_error import BaseError


class UnauthorizedError(BaseError):

    def __init__(
        self, resource_name: str, message: str | None = None, detail: dict | None = None
    ):

        self.message = f"Unauthorized on {resource_name}"
        if message:
            self.message = message

        self.detail = detail
        self.error_code = "UNAUTHORIZED"

        super().__init__(
            message=self.message, error_code=self.error_code, detail=self.detail
        )
