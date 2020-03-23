"""Product custom field value object module"""
from dataclasses import dataclass
from typing import Iterable

from src.ser.common.value_object.custom_field_value_object import CustomFieldValueObject


@dataclass
class CustomFields:
    """Blackfire custom field value object."""
    release_date: CustomFieldValueObject
    dead_line: CustomFieldValueObject

    def __iter__(self) -> Iterable[CustomFieldValueObject]:
        return iter((self.release_date, self.dead_line))
