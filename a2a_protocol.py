"""
Agent‑to‑Agent (A2A) protocol primitives.

This module defines the message envelope, intents and a simple in‑process
router to simulate A2A communication between agents.  Each message is
represented by an ``Envelope`` with sender/recipient metadata, an intent
and a payload.  The router delivers messages to registered handlers
asynchronously.  A small ``Conversation`` helper allows callers to
associate a future with a correlation ID in order to await replies.

The protocol here is deliberately minimal—real A2A systems implement
capability negotiation, authentication and streaming of multipart
messages.  This simplification suffices for demonstration purposes.
"""

from __future__ import annotations

import asyncio
import itertools
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Awaitable, Callable, Dict, Optional


class Intent(Enum):
    """Enumeration of A2A intents.

    Intents describe why a message is being sent.  The protocol used here
    supports common flows for discovery, proposals and task execution.
    """

    DISCOVER = auto()    # Request an agent card
    CARD = auto()        # Response containing an agent card
    RFP = auto()         # Request for proposal
    PROPOSE = auto()     # Proposal returned by an agent
    ACCEPT = auto()      # Accept a proposal
    REJECT = auto()      # Reject a proposal
    TASK = auto()        # Task assignment
    RESULT = auto()      # Task result
    INFO = auto()        # Informational message or status update
    ERROR = auto()       # Error message


_id = itertools.count(1)


@dataclass
class Envelope:
    """A message envelope for A2A communications.

    Each envelope carries an intent and a payload.  The correlation ID
    allows responders to link their reply to an initiating message.  The
    timestamp is recorded for auditing or ordering.
    """

    intent: Intent
    sender: str
    recipient: str
    correlation_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: f"msg-{next(_id)}")
    ts: float = field(default_factory=lambda: time.time())

    def reply(self, *, sender: str, intent: Intent, payload: Dict[str, Any]) -> "Envelope":
        """Create a reply envelope to the current message.

        The reply preserves the correlation ID if one exists, otherwise
        uses the message ID as the correlation ID.  The new message
        originates from ``sender`` and targets the original sender.
        """
        return Envelope(
            intent=intent,
            sender=sender,
            recipient=self.sender,
            correlation_id=self.correlation_id or self.message_id,
            payload=payload,
        )


class Router:
    """A simple in‑memory router for dispatching envelopes.

    Agents register their asynchronous handler functions via
    :meth:`register`.  When sending a message with :meth:`send`, the
    router looks up the handler by recipient name and awaits it.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[Envelope], Awaitable[None]]] = {}

    def register(self, address: str, handler: Callable[[Envelope], Awaitable[None]]) -> None:
        self._handlers[address] = handler

    async def send(self, env: Envelope) -> None:
        handler = self._handlers.get(env.recipient)
        if handler is None:
            raise RuntimeError(f"No handler registered for address '{env.recipient}'")
        await handler(env)


class Conversation:
    """Tracking helper for correlating requests and responses.

    A caller may call :meth:`watch` to create a future associated with a
    correlation ID.  When a reply is received, :meth:`resolve` is used
    to set the result of the future.  Consumers can ``await`` on the
    future to get their result.  This mechanism is crucial when
    concurrently awaiting multiple replies.
    """

    def __init__(self) -> None:
        self._futures: Dict[str, asyncio.Future] = {}

    def watch(self, key: str) -> asyncio.Future:
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self._futures[key] = fut
        return fut

    def resolve(self, key: str, value: Any) -> None:
        fut = self._futures.pop(key, None)
        if fut and not fut.done():
            fut.set_result(value)