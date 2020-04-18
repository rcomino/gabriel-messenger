import logging
from asyncio import Queue
from datetime import datetime

from typing import List

import facebook

from src.ser.common.data.weiss_schwarz_barcelona_data import BrigadaSOSData
from src.ser.common.enums.format_data import FormatData
from src.ser.common.itf.custom_config import CustomConfig
from src.ser.common.itf.publication import Publication
from src.ser.common.queue_manager import QueueManager
from src.ser.common.receiver_mixin import ReceiverMixin
from src.ser.common.rich_text import RichText
from src.ser.common.value_object.transacation_data import TransactionData
from src.ser.facebook.models.identifier import Identifier, METADATA


class FacebookService(ReceiverMixin, BrigadaSOSData):
    MODULE = "Facebook Receiver"
    MODEL_IDENTIFIER = Identifier
    MODELS = (Identifier,)
    MODELS_METADATA = METADATA

    _graph = None

    def __init__(self, *, files_directory: str, instance_name: str, queue_manager: QueueManager, download_files: bool,
                 wait_time: int, logging_level: str, state_change_queue: Queue, colour: int):
        self._instance_name = instance_name
        logger = logging.getLogger(self._instance_name)
        logger.setLevel(logging_level)
        super().__init__(logger=logger,
                         wait_time=wait_time,
                         state_change_queue=state_change_queue,
                         queue_manager=queue_manager,
                         files_directory=files_directory,
                         download_files=download_files)
        self._colour = colour
        self._queue_manager = queue_manager
        self._download_files = download_files
        self._files_directory = files_directory
        self._cache: List[int] = []

    # TODO: publications from web api
    # TODO: get post picture
    # TODO: save last publication date in cache instead of all published ids
    async def _load_publications(self):
        fields = "created_time,message,full_picture"
        posts = self._graph.get_connections(id='me', connection_name='posts', fields=fields, date_format="U")
        for post in posts["data"]:
            unix_time = post["created_time"]
            timestamp = datetime.fromtimestamp(unix_time)
            message = post["message"]
            # TODO: accurate format data
            description = RichText(data=message, format_data=FormatData.HTML)
            post_id = post["id"]
            if post_id not in self._cache:
                publication = Publication(publication_id=post_id,
                                          description=description,
                                          timestamp=timestamp,
                                          color=self._colour,
                                          author=self._AUTHOR)
                transaction_data = TransactionData(transaction_id=publication.publication_id,
                                                   publications=[publication])
                await self._put_in_queue(transaction_data=transaction_data)

    @classmethod
    def _get_custom_configuration(cls, *, configuration, senders):
        configurations = [
            CustomConfig(
                instance_name=cls._get_instance_name(),
                queue_manager=cls._get_queue_manager(config=configuration['send'], senders=senders),
            )
        ]
        token = configuration["token"]
        cls._graph = facebook.GraphAPI(access_token=token, version="3.1")
        return configurations
