"""DataType enum module"""
from enum import Enum


class DataType(Enum):
    """Data type enum. This is used to differentiate configuration and files, each one is save on fs on different
    directories"""
    CONFIGURATION = 'configuration'
    FILES = 'files'
