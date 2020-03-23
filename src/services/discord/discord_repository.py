"""Discord Client Module"""

import logging
from asyncio import Queue, AbstractEventLoop
from typing import Dict, Any

import discord

from src.services.common.sender_common_service_mixin import SenderCommonServiceMixin
from src.services.common.value_object.queue_data_value_object import QueueDataValueObject
from src.services.common.value_object.task_value_object import TaskValueObject
from src.services.discord.value_object.bot_config_value_object import BotConfigValueObject
from src.services.discord.value_object.channel_config_value_object import ChannelConfigValueObject
from src.services.discord.value_object.reporting_channel_config_value_object import \
    ReportingChannelConfigValueObject
from src.services.discord.value_object.reporting_channel_reaction_change_config_value_object import \
    ReportingChannelReactionChangeConfigValueObject
from src.services.discord.value_object.reporting_channel_reaction_config_value_object import \
    ReportingChannelReactionConfigValueObject


class DiscordClient(discord.Client, SenderCommonServiceMixin):
    """Discord Client."""
    MODULE = 'Discord'

    def __init__(self, *, instance_name: str, config: BotConfigValueObject, loop: AbstractEventLoop,
                 publication_queue: Queue, state_change_queue: Queue, logging_level: str):
        discord.Client.__init__(self, loop=loop)

        self._instance_name = instance_name
        self._logger = logging.getLogger(self._instance_name)
        self._logger.setLevel(logging_level)
        self._config = config
        self._publication_queue = publication_queue
        self._channels: Dict[int, discord.TextChannel] = {}
        self._publication_queue = publication_queue
        self._state_change_queue = state_change_queue

    async def on_ready(self):
        """On ready: create tasks"""
        self._logger.info("Instance is working")
        await self.change_presence(activity=self._config.activity)
        self.loop.create_task(
            self._loop_manager(
                state_change_queue=self._state_change_queue,
                logger=self._logger,
                publication_queue=self._publication_queue,
            ))

    @classmethod
    def create_tasks_from_configuration(cls, *, configuration, loop, logging_level):
        repository_instances_value_objects = {}
        for configuration_item in configuration:
            publication_queue = Queue()
            state_change_queue = Queue()

            instance_name = cls._get_instance_name()

            bot_config = BotConfigValueObject(
                activity=cls._get_activity(activity_configuration=configuration_item['activity']),
                channels_config=cls._get_channels_config(channels_config=configuration_item['channels']),
                clean_channels=configuration_item['clean_channels'],
                reporting_channels=configuration_item['reporting_channels'])
            discord_instance = cls(
                instance_name=instance_name,
                config=bot_config,
                loop=loop,
                publication_queue=publication_queue,
                state_change_queue=state_change_queue,
                logging_level=logging_level,
            )
            task = loop.create_task(discord_instance.start(configuration_item['token']), name=instance_name)

            repository_instances_value_objects[configuration_item['name']] = TaskValueObject(
                name=cls._get_instance_name(),
                state_change_queue=state_change_queue,
                publication_queue=publication_queue,
                task=task)
        return repository_instances_value_objects

    @staticmethod
    def _get_activity(activity_configuration: dict) -> discord.Activity:
        activity_type = getattr(discord.ActivityType, activity_configuration['type'])
        activity_name = activity_configuration['name']
        return discord.Activity(name=activity_name, type=activity_type)

    @classmethod
    def _get_channels_config(cls, *, channels_config: Dict[int, dict]) -> Dict[int, ChannelConfigValueObject]:
        return {
            channel_id: ChannelConfigValueObject(reactions=channel_config['reactions'],
                                                 reporting_channels_config=cls._get_reporting_channels_config(
                                                     config=channel_config['reporting_channels']))
            for channel_id, channel_config in channels_config.items()
        }

    @classmethod
    def _get_reporting_channels_config(cls, *, config: Dict[int, dict]) -> Dict[int, ReportingChannelConfigValueObject]:
        return {
            channel_id: ReportingChannelConfigValueObject(
                reactions=cls._get_reporting_channels_reactions_config(config=reporting_channels_config['reactions']),
                description=reporting_channels_config['description'],
                footer=reporting_channels_config['footer'],
            )
            for channel_id, reporting_channels_config in config.items()
        }

    @classmethod
    def _get_reporting_channels_reactions_config(
            cls, *, config: Dict[str, Any]) -> Dict[str, ReportingChannelReactionConfigValueObject]:
        return {
            reaction: ReportingChannelReactionConfigValueObject(
                text=reaction_config['text'],
                reaction_add=ReportingChannelReactionChangeConfigValueObject(
                    **(reaction_config.get('reaction_add') or {})),
                reaction_remove=ReportingChannelReactionChangeConfigValueObject(
                    **(reaction_config.get('reaction_remove') or {})),
            )
            for reaction, reaction_config in config.items()
        }

    async def _load_publication(self, *, queue_data: QueueDataValueObject) -> None:
        files = []
        embed = discord.Embed(
            title=queue_data.publication.title,
            description=queue_data.publication.description,
            url=queue_data.publication.url,
            colour=queue_data.publication.color,
        )
        if queue_data.publication.timestamp:
            embed.timestamp = queue_data.publication.timestamp

        if queue_data.publication.images:
            if queue_data.publication.images[0].public_url:
                embed.set_image(url=queue_data.publication.images[0].public_url)
            else:
                raise NotImplementedError
            if len(queue_data.publication.images) > 2:
                for image in queue_data.publication.images[1:]:
                    files.append('caca')
                    raise NotImplementedError

        for file in queue_data.publication.files:
            raise NotImplementedError

        if queue_data.publication.author:
            embed.set_author(name=queue_data.publication.author.name,
                             url=queue_data.publication.author.url,
                             icon_url=queue_data.publication.author.icon_url)

        if queue_data.publication.custom_fields:
            for field in queue_data.publication.custom_fields:
                if field:
                    embed.add_field(name=field.name, value=field.value)

        channel = await self._get_channel(channel_id=queue_data.channel)
        await channel.send(embed=embed)

    async def _get_channel(self, *, channel_id) -> discord.TextChannel:
        channel = self._channels.get(channel_id)
        if not channel:
            channel = self.get_channel(channel_id)
            self._channels[channel_id] = channel
        if not channel:
            raise EnvironmentError(f'Wrong Channel id: {channel_id}')
        return channel

    async def _close(self):
        await self.logout()

    async def on_message(self, message):
        """Receive message that some user send to discord."""
        self._logger.debug(message)
