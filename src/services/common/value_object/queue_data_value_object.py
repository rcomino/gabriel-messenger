"""Queue Data Value Object Module."""

from dataclasses import dataclass

from src.services.common.interfaces.publication_interface import PublicationInterface


@dataclass
class QueueDataValueObject:
    """Queue data value object. This value object contains all data that will put in a queue. Receivers put this value
    object in the queue. Sender service get this data and will upload this publication in the designated channel."""
    channel: int
    publication: PublicationInterface
