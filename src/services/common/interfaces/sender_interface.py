"""Sender Interface module."""

from abc import abstractmethod
from asyncio import Queue
from logging import Logger
from typing import List, Dict
import asyncio

from src.services.common.interfaces.service_interface import ServiceInterface
from src.services.common.value_object.queue_data_value_object import QueueDataValueObject
from src.services.common.value_object.task_value_object import TaskValueObject


class SenderInterface(ServiceInterface):
    """Sender Interface. This is required to implement in all sender services."""
    @classmethod
    def create_tasks_from_configuration(
            cls,
            *,
            configuration: List[dict],
            loop: asyncio.AbstractEventLoop,
            logging_level: str,
    ) -> Dict[str, TaskValueObject]:
        """Return a Dict[str, RepositoryInstanceValueObject]. String is a unique key to identify a sender, for example a
        token."""
        raise NotImplementedError

    @abstractmethod
    async def _loop_manager(self, *, state_change_queue: Queue, logger: Logger, publication_queue: Queue):
        raise NotImplementedError

    @abstractmethod
    async def _load_publication(self, *, queue_data: QueueDataValueObject) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _close(self) -> None:
        raise NotImplementedError
