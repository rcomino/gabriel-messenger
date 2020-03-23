import logging
import os
from asyncio import Queue
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.ser.common.data.weiss_schwarz_barcelona_data import WeissSchwarzBarcelonaData
from src.ser.common.itf.custom_config import CustomConfig
from src.ser.common.itf.publication import Publication
from src.ser.common.queue_manager import QueueManager
from src.ser.common.receiver_mixin import ReceiverMixin
from src.ser.ws_tournament_en.models.identifier import Identifier, METADATA


class WSTournamentEn(ReceiverMixin, WeissSchwarzBarcelonaData):
    """Weiß Schwarz - English Edition - Monthly Shop Tournament Card service. This is a receiver service.
    Get all English Edition - Monthly Shop Tournament Cards."""

    MODULE = "Weiß Schwarz - English Tournament"
    _EN_URL = 'https://en.ws-tcg.com/events/'
    MODEL_IDENTIFIER = Identifier
    MODELS = (Identifier, )
    MODELS_METADATA = METADATA

    def __init__(self, *, files_directory: str, instance_name: str, queue_manager: QueueManager, download_files: bool,
                 wait_time: int, logging_level: str, state_change_queue: Queue, colour: int):
        self._instance_name = instance_name
        logger = logging.getLogger(self._instance_name)
        logger.setLevel(logging_level)
        super().__init__(logger=logger, wait_time=wait_time, state_change_queue=state_change_queue)
        self._colour = colour
        self._queue_manager = queue_manager
        self._download_files = download_files
        self._files_directory = files_directory
        self._cache: List[str] = []

    async def _load_publications(self):
        html = await self._get_site_content(url=self._EN_URL)
        beautiful_soap = BeautifulSoup(html, 'html5lib')
        months = beautiful_soap.findAll('div', class_='monthWrap')

        for month in months:
            cards = month.findAll('img')
            title = month.find('h4').text.strip()
            for card in cards:
                publication = await self._get_new_cards(card=card, title=title)
                if publication:
                    await self._queue_manager.put(publication=publication)
                    self._logger.info("New: %s", publication.title)
                    await self.MODEL_IDENTIFIER.objects.create(id=publication.publication_id)
                    self._cache.append(publication.publication_id)

    async def _get_new_cards(self, card: Tag, title: str) -> Optional[Publication]:
        file_name = os.path.basename(card.attrs['src'])
        file_name: str = file_name.split('?')[0]
        if file_name not in self._cache:
            file = await self._get_file_value_object(url=card.attrs['src'],
                                                     download_file=self._download_files,
                                                     pretty_name=title,
                                                     files_directory=self._files_directory,
                                                     filename_unique=False,
                                                     public_url=False)

            return Publication(
                publication_id=file_name,
                title=title,
                url=self._EN_URL,
                timestamp=datetime.utcnow(),
                color=self._colour,
                images=[file],
                author=self._AUTHOR,
            )

    @classmethod
    def _get_custom_configuration(cls, *, configuration, senders):
        configurations = [
            CustomConfig(
                instance_name=cls._get_instance_name(),
                queue_manager=cls._get_queue_manager(config=configuration['send'], senders=senders),
            )
        ]
        return configurations
