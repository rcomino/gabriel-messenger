"""File Value Object Module."""
import os
from dataclasses import dataclass
from typing import Optional


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

    @property
    def filename(self):
        """Filename of file with extension."""
        if self.path:
            return os.path.basename(self.path)
        return os.path.basename(self.public_url).split('?')[0]
