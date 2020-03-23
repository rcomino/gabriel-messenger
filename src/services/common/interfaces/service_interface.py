"""Service interface module."""

from abc import abstractmethod, ABC


class ServiceInterface(ABC):
    """Service interface. This the main interface of receiver interface and sender interface."""
    @property
    @abstractmethod
    def MODULE(self) -> str:  # pylint: disable=invalid-name
        """Module name. This is used to load repository from file configuration."""
        raise NotImplementedError

    @abstractmethod
    async def run(self):
        """Run instance method."""
        raise NotImplementedError
