"""Weiss Schwarz Banner service Module."""

import logging
import os
from asyncio import Queue
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.ser.common.data.weiss_schwarz_barcelona_data import WeissSchwarzBarcelonaData
from src.ser.common.enums.language import Language
from src.ser.common.itf.publication import Publication
from src.ser.common.queue_manager import QueueManager
from src.ser.common.receiver_mixin import ReceiverMixin
from src.ser.ws_banner.models.identifier import METADATA, Identifier
from src.ser.ws_banner.data.config import Config


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
class WSBannerService(ReceiverMixin, WeissSchwarzBarcelonaData):
    """Weiss Schwarz Banner service. This is a receiver service. Get all Banners os Weiss Schwarz."""
    MODULE = 'Weiß Schwarz - Banner'
    _EN_URL = 'https://en.ws-tcg.com'
    _JP_URL = 'https://ws-tcg.com'
    _TITLE = "{} Edition - Banner"
    MODELS = (Identifier, )
    MODEL_IDENTIFIER = Identifier
    MODELS_METADATA = METADATA

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
        self._language_text = language.value
        self._title = self._TITLE.format(language.value)
        if language == Language.ENGLISH:
            self._url = self._EN_URL
        elif language == Language.JAPANESE:
            self._url = self._JP_URL
        else:
            raise NotImplementedError

    async def _load_publications(self):
        html = await self._get_site_content(url=self._url)
        beautiful_soap = BeautifulSoup(html, 'html5lib')
        banners = beautiful_soap.findAll('div', class_='slide-banner')[0].findAll('img')

        for banner in banners:
            publication = await self._get_banners(banner=banner)
            if publication:
                await self._queue_manager.put(publication=publication)
                self._logger.info("New: %s", publication.title)
                await Identifier.objects.create(id=publication.publication_id)
                self._cache.append(publication.publication_id)

    async def _get_banners(self, banner: Tag) -> Optional[Publication]:
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

                return Publication(
                    publication_id=filename,
                    title=self._title,
                    url=self._url,
                    timestamp=datetime.utcnow(),
                    color=self._colour,
                    images=[file],
                    author=self._AUTHOR,
                )

    @classmethod
    def _get_custom_configuration(cls, *, configuration, senders):
        configurations = []
        for language_text, sender_config in configuration['send'].items():
            language = Language(language_text)
            configurations.append(
                Config(
                    language=language,
                    instance_name=cls._get_instance_name(language_text),
                    queue_manager=cls._get_queue_manager(config=sender_config, senders=senders),
                ))
        return configurations
