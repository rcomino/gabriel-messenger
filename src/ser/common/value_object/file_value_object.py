"""File Value Object Module."""
import io
import os
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass
from typing import Optional

from aiofile import AIOFile


@dataclass
class FileValueObject:
    """This value object is abstraction how app need to interact with a file. It's possible that is only available on
    file system or a public url."""
    public_url: str = None
    path: Optional[str] = None
    pretty_name: str = None

    @property
    def pretty_filename(self):
        """Return a pretty filename if it's possible. Is possible when pretty_name is fulfilled."""
        if self.pretty_name:
            if self.path:
                extension = os.path.basename(self.path).split('.')[1].split('?')[0]
            else:
                extension = os.path.basename(self.public_url).split('.')[1]
            return f"{self.pretty_name}.{extension}"
        return os.path.basename(self.public_url)

    @asynccontextmanager
    async def file_obj(self, mode) -> AIOFile:
        async with AIOFile(self.path, mode) as afp:
            yield afp

    async def bytes_io(self) -> io.BytesIO:
        async with AIOFile(self.path, 'rb') as afp:
            data = io.BytesIO(await afp.read())
        return data

    @property
    def filename(self):
        if self.path:
            return os.path.basename(self.path)
        return os.path.basename(self.public_url).split('?')[0]
