"""Product Value Object Module"""
from dataclasses import dataclass
from typing import Optional

from src.ser.blackfire.data.custom_fields import CustomFields
from src.ser.common.itf.publication import Publication


@dataclass
class BlackfirePublication(Publication):
    """Dataclass that expand a Publication."""
    custom_fields: Optional[CustomFields] = None

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
