import logging
import requests
from asyncio import Queue
from datetime import datetime

from typing import List

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
    _BASE_URL = "https://graph.facebook.com/{0}/feed?" \
                "date_format=U&" \
                "fields=created_time,message,full_picture&" \
                "access_token={1}"

    _url = None

    def __init__(self, *, files_directory: str, instance_name: str, queue_manager: QueueManager, download_files: bool,
                 wait_time: int, logging_level: str, state_change_queue: Queue, colour: int):
        self._instance_name = instance_name
        self.logger = logging.getLogger(self._instance_name)
        self.logger.setLevel(logging_level)
        super().__init__(logger=self.logger,
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

    # TODO: save last publication date in cache instead of all published ids
    async def _load_publications(self):
        resp = requests.get(self._url)
        if resp.status_code != 200:
            error = resp.json()["error"]
            error_code = error["code"]
            if error_code == 190:
                self.logger.error("Access token expired")
            else:
                self.logger.error("Could not load Facebook publications. Status code {}".format(resp.status_code))
        else:
            post_result = resp.json()
            post_list = sorted(post_result["data"], key=lambda p: p["created_time"])
            for post in post_list:
                unix_time = post["created_time"]
                timestamp = datetime.fromtimestamp(unix_time)
                message = post["message"]
                # TODO: accurate format data
                description = RichText(data=message, format_data=FormatData.HTML)
                post_id = post["id"]
                images = []
                if "full_picture" in post:
                    img_url = post["full_picture"]
                    img = await self._get_file_value_object(url=img_url, public_url=True, filename_unique=True)
                    images.append(img)

                if post_id not in self._cache:
                    publication = Publication(publication_id=post_id,
                                              description=description,
                                              timestamp=timestamp,
                                              color=self._colour,
                                              images=images,
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
        page_id = configuration["page_id"]
        cls._url = cls._BASE_URL.format(page_id, token)
        return configurations
