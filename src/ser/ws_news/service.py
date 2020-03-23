import logging
from asyncio import Queue
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup, element

from src.ser.common.data.weiss_schwarz_barcelona_data import WeissSchwarzBarcelonaData
from src.ser.common.itf.custom_config import CustomConfig
from src.ser.common.itf.publication import Publication
from src.ser.common.queue_manager import QueueManager
from src.ser.common.receiver_mixin import ReceiverMixin
from src.ser.ws_tournament_jp.models.identifier import Identifier, METADATA


class WSNews(ReceiverMixin, WeissSchwarzBarcelonaData):
    """Weiß Schwarz - News. This is a receiver service. Get news."""

    MODULE = "Weiß Schwarz - News"
    _URL = 'https://en.ws-tcg.com/information/'
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
        html = await self._get_site_content(url=self._URL)
        beautiful_soap = BeautifulSoup(html, 'html5lib')
        news = beautiful_soap.find('ul', class_='info-list').find_all('li')

        for new in news:
            publication = await self._get_new_new(new=new)
            if publication:
                await self._queue_manager.put(publication=publication)
                self._logger.info("New: %s", publication.title)
                await self.MODEL_IDENTIFIER.objects.create(id=publication.publication_id)
                self._cache.append(publication.publication_id)

    async def _get_new_new(self, new: element.Tag) -> Optional[Publication]:
        url = new.find('a').attrs['href']

        if url not in self._cache:
            images = []
            url = new.find('img').attrs['src'].split('?')[0]
            title = new.find(class_='title').text
            new.find('img')
            file = await self._get_file_value_object(url=url,
                                                     download_file=self._download_files,
                                                     pretty_name=title,
                                                     files_directory=self._files_directory,
                                                     filename_unique=False,
                                                     public_url=False)
            images.append(file)

            return Publication(
                publication_id=file_name,
                title=title,
                url=self._EN_URL,
                timestamp=datetime.utcnow(),
                color=self._colour,
                images=images,
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
