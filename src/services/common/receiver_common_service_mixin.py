"""Receiver Common Service Mixin Module."""

import asyncio
import os
from abc import abstractmethod
from asyncio import Queue, QueueEmpty
import time
from logging import Logger
from typing import Dict, List

import aiofiles
import aiohttp
import appdirs
import databases
import sqlalchemy
from orm.models import ModelMetaclass
from sqlalchemy import MetaData

from src.services.common.common_repository_mixin import CommonRepositoryMixin
from src.services.common.enums.environment import Environment
from src.services.common.enums.state import State
from src.services.common.interfaces.receiver_interface import ReceiverInterface
from src.services.common.queue_manager import QueueManager
from src.services.common.value_object.file_value_object import FileValueObject
from src.services.common.value_object.queue_context_value_object import QueueContextValueObject
from src.services.common.value_object.task_value_object import TaskValueObject


class ReceiverCommonServiceMixin(ReceiverInterface, CommonRepositoryMixin):
    """Receiver Common Service Mixin. This mixin include methods required by receivers services."""
    def __init__(self, logger: Logger, wait_time: int, state_change_queue: Queue):
        self._logger = logger
        self._wait_time = wait_time
        self._state_change_queue = state_change_queue

    @classmethod
    def _get_queue_manager(cls, config: Dict[str, dict], senders: Dict[str, Dict[str, TaskValueObject]]):
        queue_context_list = []
        for sender_name, senders_configs in config.items():
            for sender_id, sender_configs in senders_configs.items():
                for channel in sender_configs:
                    queue_context = QueueContextValueObject(
                        channel=channel, publication_queue=senders[sender_name][sender_id].publication_queue)
                    queue_context_list.append(queue_context)
        return QueueManager(queue_context_list=queue_context_list)

    @classmethod
    def _get_repository_directory(cls, *, app_name: str, environment: Environment):
        repository_directory = os.path.join(appdirs.user_data_dir(app_name), environment.value, cls.MODULE)
        os.makedirs(repository_directory, exist_ok=True)
        return repository_directory

    @classmethod
    def _set_database(cls, *, metadata: MetaData, models: List[ModelMetaclass], app_name: str,
                      environment: Environment):
        repository_directory = cls._get_repository_directory(app_name=app_name, environment=environment)
        database_file = os.path.join(repository_directory, cls._DATABASE_FILE)
        database = databases.Database("sqlite:///" + database_file)

        for model in models:
            model.__database__ = database
        engine = sqlalchemy.create_engine(str(database.url), connect_args={'timeout': 6000000})
        metadata.create_all(engine, checkfirst=True)

    @classmethod
    def _get_repository_files_directory(cls, app_name: str, environment: Environment):
        repository_directory = cls._get_repository_directory(app_name=app_name, environment=environment)
        files_directory = os.path.join(repository_directory, cls._FILES_DIRECTORY)
        os.makedirs(files_directory, exist_ok=True)
        return files_directory

    async def _loop_manager(self, *, wait_time: int, state_change_queue: Queue, logger: Logger):
        start = 0
        while True:
            try:
                new_state: State = state_change_queue.get_nowait()
                if new_state == State.STOP:
                    logger.info("Shutdown")
                    return
                raise NotImplementedError
            except QueueEmpty:
                logger.debug("No new state.")

            if (time.time() - start) > wait_time:
                await self._load_publications()
                logger.debug("Waiting %s seconds", wait_time)
                start = time.time()
            else:
                await asyncio.sleep(self._WAIT_TIME)
                logger.debug("Remains %s seconds, to execute the task.", int(wait_time - (time.time() - start)))

    @abstractmethod
    async def _load_publications(self) -> None:
        raise NotImplementedError

    @staticmethod
    async def _get_file_value_object(url: str,
                                     files_directory: str,
                                     download_file: bool,
                                     pretty_name=None) -> FileValueObject:
        if not download_file:
            return FileValueObject(
                public_url=url,
                pretty_name=pretty_name,
            )
        filename = os.path.basename(url)
        path = os.path.join(files_directory, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                async with aiofiles.open(path, mode='wb') as file:
                    await file.write(await resp.read())
        return FileValueObject(
            path=path,
            public_url=url,
            pretty_name=pretty_name,
        )

    async def run(self):
        self._logger.info("Instance is working")
        await self._load_cache()
        await self._loop_manager(wait_time=self._wait_time,
                                 state_change_queue=self._state_change_queue,
                                 logger=self._logger)

    @staticmethod
    async def _get_site_content(*, url) -> bytes:
        """This method get a url and return content in bytes."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response = await resp.read()
                return response

    @classmethod
    def create_tasks_from_configuration(cls, *, configuration, senders, loop, app_name, environment, logging_level):
        files_directory = cls._get_repository_files_directory(app_name=app_name, environment=environment)
        cls._set_database(models=[
            Product,
        ], metadata=METADATA, app_name=app_name, environment=environment)
        instance_value_objects: List[TaskValueObject] = []
        for search_parameters, sender_config in configuration['search'].items():
            search_parameters_encoded = urllib.parse.quote(search_parameters)
            state_change_queue = Queue()
            instance_name = cls._get_instance_name(search_parameters)
            task = loop.create_task(cls(
                colour=configuration['colour'],
                files_directory=files_directory,
                instance_name=instance_name,
                queue_manager=cls._get_queue_manager(config=sender_config, senders=senders),
                search_parameters=search_parameters_encoded,
                wait_time=configuration['wait_time'],
                download_files=configuration['download_files'],
                logging_level=logging_level,
                state_change_queue=state_change_queue,
            ).run(),
                                    name=instance_name)
            instance_value_objects.append(
                TaskValueObject(
                    name=instance_name,
                    task=task,
                    state_change_queue=state_change_queue,
                ))

        return instance_value_objects
