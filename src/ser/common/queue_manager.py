"""Queue Manager Module."""

from dataclasses import dataclass
from typing import List

from src.ser.common.itf.publication import Publication
from src.ser.common.value_object.queue_context import QueueContext
from src.ser.common.value_object.queue_data import QueueData


@dataclass
class QueueManager:
    """Queue Manager. Instance will be passed a receiver service. This is the one in charge to manage queues."""
    queue_context_list: List[QueueContext]

    async def put(self, publication: Publication):
        """For item in queue context list (channel, queue) upload in the queue a QueueData
        (channel, publication)"""
        for queue_context in self.queue_context_list:
            queue_data = QueueData(channel=queue_context.channel, publication=publication)
            await queue_context.publication_queue.put(queue_data)
