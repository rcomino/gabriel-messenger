"""Custom Field Value Object Module."""
from dataclasses import dataclass


@dataclass
class CustomField:
    """Custom Field Value Object. This describes a custom field and his value. Each receiver can add custom fields that
    will be attached in a Publication."""
    value: str
    name: str
