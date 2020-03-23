"""Receiver Interface module."""
import asyncio
from abc import abstractmethod
from asyncio import Queue
from logging import Logger
from typing import List, Dict

from src.services.common.enums.environment import Environment
from src.services.common.interfaces.service_interface import ServiceInterface
from src.services.common.value_object.task_value_object import TaskValueObject


class ReceiverInterface(ServiceInterface):
    """Receiver Interface. Receiver is a service that download data from web and pass to sender service."""
    @classmethod
    def create_tasks_from_configuration(
            cls,
            *,
            configuration: dict,
            senders: Dict[str, Dict[str, TaskValueObject]],
            loop: asyncio.AbstractEventLoop,
            app_name: str,
            environment: Environment,
            logging_level: str,
    ) -> List[TaskValueObject]:
        """Create asyncio tasks in loop, this method can generate several tasks. Return RepositoryInstanceValueObject
        that allow to control the state of each task."""
        raise NotImplementedError

    @abstractmethod
    async def _load_publications(self) -> None:
        """Function called to get new publications and put in the corresponding publication queue."""
        raise NotImplementedError

    @abstractmethod
    async def _loop_manager(self, *, wait_time: int, state_change_queue: Queue, logger: Logger) -> None:
        """Function that control task loop. This function is also required that control change state queue."""
        raise NotImplementedError

    @abstractmethod
    async def _load_cache(self) -> None:
        """Function that load cache."""
        raise NotImplementedError
