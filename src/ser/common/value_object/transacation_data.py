"""Transaction Data Module."""

from dataclasses import dataclass
from typing import Union, List

from src.ser.common.itf.publication import Publication


@dataclass
class TransactionData:
    """All required data, to create a transaction. A transaction in these cases is to know if a sender send a block of
    publications to all queues configured."""
    transaction_id: Union[str, int]
    publications: List[Publication]
