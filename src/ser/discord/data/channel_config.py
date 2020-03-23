"""Channel Config Value Object."""

from dataclasses import dataclass
from typing import List, Dict

from src.ser.discord.data.reporting_channel_config import \
    ReportingChannelConfig


@dataclass
class ChannelConfig:
    """Channel Config Value Object. Configuration of channel."""
    reactions: List[str]
    reporting_channels_config: Dict[int, ReportingChannelConfig]
