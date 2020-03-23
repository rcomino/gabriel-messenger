"""Queue Manager Module."""

from dataclasses import dataclass
from typing import List

from src.services.common.interfaces.publication_interface import PublicationInterface
from src.services.common.value_object.queue_context_value_object import QueueContextValueObject
from src.services.common.value_object.queue_data_value_object import QueueDataValueObject


@dataclass
class QueueManager:
    """Queue Manager. Instance will be passed a receiver service. This is the one in charge to manage queues."""
    queue_context_list: List[QueueContextValueObject]

    async def put(self, publication: PublicationInterface):
        """For item in queue context list (channel, queue) upload in the queue a QueueDataValueObject
        (channel, publication)"""
        for queue_context in self.queue_context_list:
            queue_data = QueueDataValueObject(channel=queue_context.channel, publication=publication)
            await queue_context.publication_queue.put(queue_data)
