class AppError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"AppError: {self.message} (status: {self.status_code})"

    def print_error(self):
        print(str(self))