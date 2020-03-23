"""Bot config value object."""
from dataclasses import dataclass
from typing import Dict, List

import discord

from src.ser.discord.data.channel_config import ChannelConfig


@dataclass
class BotConfig:
    """Bot Config value object."""
    activity: discord.Activity
    channels_config: Dict[int, ChannelConfig]
    clean_channels: List[int]
    reporting_channels: List[int]
