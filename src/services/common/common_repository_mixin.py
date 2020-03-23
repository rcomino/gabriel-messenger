"""Common Repository Mixin Module."""


# pylint: disable=too-few-public-methods
class CommonRepositoryMixin:
    """Common Repository Mixin. This class includes methods that required by senders services and receivers services."""
    _DATABASE_FILE = "db.sqlite"
    _FILES_DIRECTORY = 'files'
    _WAIT_TIME = 5

    @classmethod
    def _get_instance_name(cls, *args):
        if args:
            return f"{cls.MODULE} [{' '.join(args)}]"
        return f"{cls.MODULE}"
