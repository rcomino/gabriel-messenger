"""Sender Common Service Mixin Module"""

import asyncio
from abc import abstractmethod
from asyncio import Queue, QueueEmpty
from logging import Logger

from src.services.common.common_repository_mixin import CommonRepositoryMixin
from src.services.common.enums.state import State
from src.services.common.interfaces.sender_interface import SenderInterface
from src.services.common.value_object.queue_data_value_object import QueueDataValueObject


class SenderCommonServiceMixin(SenderInterface, CommonRepositoryMixin):
    """Sender Common Service Mixin. This mixin include methods required by senders services."""
    async def _loop_manager(self, *, state_change_queue: Queue, logger: Logger, publication_queue: Queue):
        while True:
            try:
                queue_data: QueueDataValueObject = publication_queue.get_nowait()
                await self._load_publication(queue_data=queue_data)
            except QueueEmpty:
                logger.debug("No publications.")
                try:
                    new_state: State = state_change_queue.get_nowait()
                    if new_state == State.STOP:
                        await self._close()
                        logger.info("Shutdown.")
                        return
                    raise NotImplementedError
                except QueueEmpty:
                    logger.debug("No new state.")

            await asyncio.sleep(self._WAIT_TIME)

    @abstractmethod
    async def _load_publication(self, *, queue_data) -> None:
        raise NotImplementedError
