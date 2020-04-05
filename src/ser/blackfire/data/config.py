"""Blackfire Custom Config Module."""

from dataclasses import dataclass

from src.ser.common.itf.custom_config import CustomConfig


@dataclass
class Config(CustomConfig):
    """Blackfire custom config."""
    search_parameters: str
