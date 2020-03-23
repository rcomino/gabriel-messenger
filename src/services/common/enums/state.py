"""State enum module"""
from enum import Enum


class State(Enum):
    """State enum. This is used to change state of a service. Default state is normal."""
    NORMAL = 'normal'
    STOP = 'stop'
