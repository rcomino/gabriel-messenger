"""Reporting Channel Reaction Config Value Object Module."""

from dataclasses import dataclass

from src.services.discord.value_object.reporting_channel_reaction_change_config_value_object import \
    ReportingChannelReactionChangeConfigValueObject


@dataclass
class ReportingChannelReactionConfigValueObject:
    """Reporting Channel Reaction Change Config Value Object. Configuration when someone add or remove a reaction of a
    event message."""
    text: str
    reaction_add: ReportingChannelReactionChangeConfigValueObject
    reaction_remove: ReportingChannelReactionChangeConfigValueObject
