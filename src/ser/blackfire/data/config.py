from dataclasses import dataclass

from src.ser.common.itf.custom_config import CustomConfig


@dataclass
class Config(CustomConfig):
    search_parameters: str
