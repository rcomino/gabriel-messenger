from abc import ABC
from dataclasses import dataclass

from src.ser.common.queue_manager import QueueManager


@dataclass
class CustomConfig(ABC):
    instance_name: str
    queue_manager: QueueManager
