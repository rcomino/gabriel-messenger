"""Publication Interface module."""

from abc import abstractmethod, ABC
from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Optional, Union, Any

from src.ser.common.value_object.author_value_object import AuthorValueObject
from src.ser.common.value_object.file_value_object import FileValueObject


# pylint: disable=too-many-instance-attributes
@dataclass
class Publication(ABC):
    """Publication Interface. Is the base to create another dataclass that will be used to share publications between
    services."""
    publication_id: Union[str, int]
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    color: Optional[int] = None
    images: List[FileValueObject] = field(default_factory=list)
    files: List[FileValueObject] = field(default_factory=list)
    author: Optional[AuthorValueObject] = None
    custom_fields: Optional[Any] = None

    @property
    def markdown(self):
        return f"*{self.title}*\n"

    @property
    def text(self):
        return "{self.title}*\n"
