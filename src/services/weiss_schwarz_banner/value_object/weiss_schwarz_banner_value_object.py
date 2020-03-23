"""Weiss Schwarz Banner Value Object Module."""

from dataclasses import dataclass

from src.services.common.interfaces.publication_interface import PublicationInterface


@dataclass
class WeissSchwarzBannerValueObject(PublicationInterface):
    """Dataclass that expand a Publication."""
    @property
    def markdown(self):
        return \
            f"*{self.title}*\n"

    @property
    def text(self):
        return \
            f"{self.title}*\n"
