"""Custom service configuration Module."""

from dataclasses import dataclass

from src.ser.common.enums.language import Language
from src.ser.common.itf.custom_config import CustomConfig


@dataclass
class Config(CustomConfig):
    """Custom service configuration."""
    language: Language
