from abc import ABC, abstractmethod
from vk_api import VkApi
from toaster.broker.events import Event
from toaster.keyboards import SnackbarAnswer


class BaseAction(ABC):
    """Command handler base class."""

    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api

    def __call__(self, event: Event) -> bool:
        return self._handle(event)

    @abstractmethod
    def _handle(self, event: Event) -> bool:
        """DOCSTRING"""

    def snackbar(self, event: dict, text: str):
        """Sends a snackbar to the user.

        Args:
            event (ButtonEvent): VK button_pressed custom event.
            text (str): Sncakbar text.
        """
        self.api.messages.sendMessageEventAnswer(
            event_id=event.button.beid,
            user_id=event.user.uuid,
            peer_id=event.peer.bpid,
            event_data=SnackbarAnswer(text).data,
        )
