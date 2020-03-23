"""Product custom field value object module"""
from dataclasses import dataclass
from typing import Iterable

from src.services.common.value_object.custom_field_value_object import CustomFieldValueObject


@dataclass
class ProductCustomFieldsValueObject:
    """Product custom field value object. This ara custom fields of """
    release_date: CustomFieldValueObject
    dead_line: CustomFieldValueObject

    def __iter__(self) -> Iterable[CustomFieldValueObject]:
        return iter((self.release_date, self.dead_line))
