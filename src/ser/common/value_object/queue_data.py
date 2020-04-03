"""Queue Data Value Object Module."""

from dataclasses import dataclass

from src.ser.common.itf.publication import Publication


@dataclass
class QueueData:
    """Queue data value object. This value object contains all data that will put in a queue. Receivers put this value
    object in the queue. Sender service get this data and will upload this publication in the designated channel."""
    channel: int
    publication: Publication
