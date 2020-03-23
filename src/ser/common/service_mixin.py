"""Common Repository Mixin Module."""
from abc import abstractmethod


# pylint: disable=too-few-public-methods
class ServiceMixin:
    """Common Service Mixin. This class includes methods that required by senders services and receivers services."""
    MODULE = NotImplementedError  # type: str
    _DATABASE_FILE = "db.sqlite"
    _FILES_DIRECTORY = 'files'
    _WAIT_TIME = 5

    @classmethod
    def _get_instance_name(cls, *args):
        if args:
            return f"{cls.MODULE} [{' '.join(args)}]"
        return f"{cls.MODULE}"

    @abstractmethod
    async def run(self):
        """Run instance method."""
        raise NotImplementedError
