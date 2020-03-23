"""Product Value Object Module"""
from dataclasses import dataclass
from typing import Optional

from src.services.blackfire.value_object.product_custom_fields_value_object import ProductCustomFieldsValueObject
from src.services.common.interfaces.publication_interface import PublicationInterface


@dataclass
class ProductValueObject(PublicationInterface):
    """Dataclass that expand a Publication."""
    custom_fields: Optional[ProductCustomFieldsValueObject] = None

    @property
    def markdown(self):
        return \
            f"*{self.title}*\n" \
            f"{self.description}" \
            f"Release Date: {self.custom_fields.release_date.value}\n" \
            f"Dead line: {self.custom_fields.dead_line.value}"

    @property
    def text(self):
        return \
            f"{self.title}*\n" \
            f"{self.description}" \
            f"Release Date: {self.custom_fields.release_date.value}\n" \
            f"Dead line: {self.custom_fields.dead_line.value}"
