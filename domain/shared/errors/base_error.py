class BaseError(Exception):

    def __init__(self, message: str, error_code: str, detail: dict | None = None):
        self.message = message
        self.detail = detail
        self.error_code = error_code

        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "detail": self.detail,
            "error_code": self.error_code,
        }
