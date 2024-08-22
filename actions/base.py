"""Module "actions".

File:
    base.py

About:
    Initializing the "actions" module.
"""

from abc import ABC, abstractmethod
from vk_api import VkApi
from funcka_bots.broker.events import BaseEvent
from funcka_bots.keyboards import SnackbarAnswer


class BaseAction(ABC):
    """Base class of the bot button response action."""

    NAME = "None"

    def __init__(self, api: VkApi) -> None:
        self.api = api

    def __call__(self, event: BaseEvent) -> bool:
        return self._handle(event)

    @abstractmethod
    def _handle(self, event: BaseEvent) -> bool:
        """The main function of action execution.

        Args:
            event (Event): Custom Event object.

        Returns:
            bool: Execution status.
        """

    def snackbar(self, event: BaseEvent, text: str) -> None:
        """Sends a snackbar to the user.

        Args:
            event (Event): Custom Event object.
            text (str): Sncakbar text.
        """

        self.api.messages.sendMessageEventAnswer(
            event_id=event.button.beid,
            user_id=event.user.uuid,
            peer_id=event.peer.bpid,
            event_data=SnackbarAnswer(text).data,
        )
