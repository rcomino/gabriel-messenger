"""Custom Config Module."""

from abc import ABC
from dataclasses import dataclass

from src.ser.common.queue_manager import QueueManager


@dataclass
class CustomConfig(ABC):
    """Custom Configuration of a receiver service. Each receiver service can add some other values."""
    instance_name: str
    queue_manager: QueueManager
