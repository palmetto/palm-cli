class AbortPalm(Exception):
    pass


class NoRepositoryError(Exception):
    """
    Raised when a git repository is not found.
    """

    pass


class InvalidConfigError(Exception):
    """
    Raised when the config is invalid.
    """

    def __init__(self, message: str = "Invalid config"):
        self.message = message
        super().__init__(self.message)
