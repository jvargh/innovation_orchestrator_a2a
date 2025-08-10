"""
Agent registry utilities.

The registry maps human‑friendly names to addresses.  Each address
represents an endpoint for A2A communication.  In a real system, an
address might be a URL or network identifier; in this demo we use
simple string identifiers.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Address:
    """Unique address for an agent within the router."""
    name: str


class Registry:
    """Stores mapping between names and Address objects."""

    def __init__(self) -> None:
        self._addresses: Dict[str, Address] = {}

    def addr(self, name: str) -> Address:
        if name not in self._addresses:
            self._addresses[name] = Address(name=name)
        return self._addresses[name]