class ConfigError(Exception):

    def __init__(self, message: str = "Invalid bot config"):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"ConfigError: {self.message}"
