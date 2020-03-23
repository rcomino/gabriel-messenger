"""Weiss Schwarz Banner service Module."""

import asyncio
import logging
import os
from asyncio import Queue
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.services.common.data.weiss_schwarz_barcelona_data import WeissSchwarzBarcelonaData
from src.services.common.enums.language import Language
from src.services.common.queue_manager import QueueManager
from src.services.common.receiver_common_service_mixin import ReceiverCommonServiceMixin
from src.services.common.value_object.task_value_object import TaskValueObject
from src.services.weiss_schwarz_banner.models.weiss_schwarz_banner import METADATA, \
    WeissSchwarzBanner
from src.services.weiss_schwarz_banner.value_object.weiss_schwarz_banner_value_object import \
    WeissSchwarzBannerValueObject


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
class WeissSchwarzBannerService(ReceiverCommonServiceMixin, WeissSchwarzBarcelonaData):
    """Weiss Schwarz Banner service. This is a receiver service. Get all Banners os weiss Schwarz."""
    MODULE = 'Weiß Schwarz - Banner'
    _EN_URL = 'https://en.ws-tcg.com'
    _JP_URL = 'https://ws-tcg.com'
    _TITLE = "New Product"

    def __init__(self, *, files_directory: str, instance_name: str, queue_manager: QueueManager, language: Language,
                 download_files: bool, wait_time: int, logging_level: str, state_change_queue: Queue, colour: int):
        self._instance_name = instance_name
        logger = logging.getLogger(self._instance_name)
        logger.setLevel(logging_level)
        super().__init__(logger=logger, wait_time=wait_time, state_change_queue=state_change_queue)
        self._colour = colour
        self._queue_manager = queue_manager
        self._download_files = download_files
        self._files_directory = files_directory
        self._cache: List[int] = []

        if language == Language.ENGLISH:
            self._url = self._EN_URL
        elif language == Language.JAPANESE:
            self._url = self._JP_URL
        else:
            raise NotImplementedError

    @classmethod
    def create_tasks_from_configuration(cls, *, configuration, senders, loop, app_name, environment, logging_level):
        files_directory = cls._get_repository_files_directory(app_name=app_name, environment=environment)
        cls._set_database(models=[
            WeissSchwarzBanner,
        ], metadata=METADATA, app_name=app_name, environment=environment)
        instance_value_objects: List[TaskValueObject] = []
        for language_text, sender_config in configuration['send'].items():
            language = Language(language_text)
            state_change_queue = Queue()
            instance_name = cls._get_instance_name()
            task = loop.create_task(cls(
                colour=configuration['colour'],
                files_directory=files_directory,
                instance_name=instance_name,
                queue_manager=cls._get_queue_manager(config=sender_config, senders=senders),
                wait_time=configuration['wait_time'],
                download_files=configuration['download_files'],
                logging_level=logging_level,
                state_change_queue=state_change_queue,
                language=language,
            ).run(),
                                    name=instance_name)
            instance_value_objects.append(
                TaskValueObject(
                    name=instance_name,
                    task=task,
                    state_change_queue=state_change_queue,
                ))

        return instance_value_objects

    async def _load_cache(self) -> None:
        self._cache = [announcement.id for announcement in await WeissSchwarzBanner.objects.all()]

    async def _load_publications(self):
        html = await self._get_site_content(url=self._url)
        beautiful_soap = BeautifulSoup(html, 'html.parser')
        banners = beautiful_soap.find_all('div', class_='slide-banner')[0].find_all('img')

        publications = await asyncio.gather(*[self._get_banners(banner=banner) for banner in banners])
        for publication in publications:
            if publication:
                await self._queue_manager.put(publication=publication)
                self._logger.info("New Banner: %s", publication.title)
                await WeissSchwarzBanner.objects.create(id=publication.publication_id)

    async def _get_banners(self, banner: Tag) -> Optional[WeissSchwarzBannerValueObject]:
        filename = os.path.basename(banner['src'].split('?')[0])
        if filename not in self._cache:
            pretty_name = None
            if 'alt' in banner:
                pretty_name = banner['alt'] if banner['alt'] else None
            if filename not in self._cache:
                self._logger.debug("Download: %s", pretty_name or filename)
                file = await self._get_file_value_object(url=banner['src'],
                                                         download_file=self._download_files,
                                                         pretty_name=pretty_name,
                                                         files_directory=self._files_directory)
                return WeissSchwarzBannerValueObject(
                    publication_id=filename,
                    title=pretty_name or self._TITLE,
                    url=self._url,
                    timestamp=datetime.utcnow(),
                    color=self._colour,
                    images=[file],
                    author=self._AUTHOR,
                )
