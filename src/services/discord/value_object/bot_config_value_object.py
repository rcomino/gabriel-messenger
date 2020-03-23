"""Bot config value object."""
from dataclasses import dataclass
from typing import Dict, List

import discord

from src.services.discord.value_object.channel_config_value_object import ChannelConfigValueObject


@dataclass
class BotConfigValueObject:
    """Bot Config value object."""
    activity: discord.Activity
    channels_config: Dict[int, ChannelConfigValueObject]
    clean_channels: List[int]
    reporting_channels: List[int]
