from domain.shared.errors.base_error import BaseError


class ForbiddenError(BaseError):

    def __init__(
        self, resource_name: str, message: str | None = None, detail: dict | None = None
    ):

        self.message = f"Forbidden error on {resource_name}"
        if message:
            self.message = message

        self.detail = detail
        self.error_code = "UNAUTHORIZED"

        super().__init__(
            message=self.message, error_code=self.error_code, detail=self.detail
        )
