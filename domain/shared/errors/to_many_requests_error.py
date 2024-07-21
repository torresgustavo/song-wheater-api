from domain.shared.errors.base_error import BaseError


class ToManyRequestsError(BaseError):

    def __init__(
        self, resource_name: str, message: str | None = None, detail: dict | None = None
    ):

        self.message = f"To many requests on {resource_name}, take a time"
        if message:
            self.message = message

        self.detail = detail
        self.error_code = "TO_MANY_REQUESTS"

        super().__init__(
            message=self.message, error_code=self.error_code, detail=self.detail
        )
