from domain.shared.errors.base_error import BaseError


class NotFoundError(BaseError):

    def __init__(
        self, resource_name: str, message: str | None = None, detail: dict | None = None
    ):

        self.message = f"{resource_name} not found"
        self.detail = detail
        self.error_code = "NOT_FOUND"

        if message:
            self.message = message

        super().__init__(
            message=self.message, error_code=self.error_code, detail=self.detail
        )
