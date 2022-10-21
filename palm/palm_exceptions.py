class AbortPalm(Exception):
    pass


class NoRepositoryError(Exception):
    """
    Raised when a git repository is not found.
    """

    pass
