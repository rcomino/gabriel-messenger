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
from src.ser.ws_tournament_jp.models.identifier import Identifier, METADATA


class WSTournamentJp(ReceiverMixin, WeissSchwarzBarcelonaData):
    """Weiß Schwarz - Japanese Edition - Tournament. This is a receiver service.
    Get data of Japanese - Monthly Shop Tournament Cards."""

    MODULE = "Weiß Schwarz - Japanese Tournament"
    _JP_URL = 'https://ws-tcg.com/events/list/battle_{}'
    _TITLE = "Japanese Edition - Monthly Shop Tournament Card"
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
        self._cache: List[int] = []

    async def _load_publications(self):
        if not self._cache:
            self._cache = [850]
        while True:
            ws_id = max(self._cache) + 1
            url = self._JP_URL.format(ws_id)
            html = await self._get_site_content(url=url)
            beautiful_soap = BeautifulSoup(html, 'html5lib')
            main = images = beautiful_soap.find('div', class_='contents-box-main')

            if not main:
                self._logger.debug("No more entries.")
                return
            images = main.find_all('img')

            for image in images:
                publication = await self._get_new_cards(card=image, url=url)
                if publication:
                    await self._queue_manager.put(publication=publication)
                    self._logger.info("New: %s", publication.title)
                    self._cache.append(ws_id)
                else:
                    pass
            await self.MODEL_IDENTIFIER.objects.create(id=ws_id)

    async def _get_new_cards(self, card: Tag, url: str) -> Optional[Publication]:
        file_name = os.path.basename(card.attrs['src'])
        file_name: str = file_name.split('?')[0]
        if file_name not in self._cache:
            file = await self._get_file_value_object(url=card.attrs['src'],
                                                     download_file=self._download_files,
                                                     pretty_name=self._TITLE,
                                                     files_directory=self._files_directory,
                                                     filename_unique=False,
                                                     public_url=False)

            return Publication(
                publication_id=file_name,
                title=self._TITLE,
                url=url,
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
