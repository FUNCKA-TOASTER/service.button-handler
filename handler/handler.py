"""Module "handler".

File:
    handler.py

About:
    File describing button handler class.
"""

from typing import NoReturn, Optional, Any, Union, Dict
from loguru import logger
from vk_api import VkApi
from funcka_bots.broker.events import Event
from actions import action_list
import config


Payload = Dict[str, Union[str, int]]
ExecResult = Optional[Union[bool, NoReturn]]


class ButtonHandler:
    """Button handler class"""

    def __call__(self, event: Event) -> None:
        try:
            payload = self._get_payload(event)

            self._check_owner(payload, event)

            action_name = payload.get("action_name")
            if self._execute(action_name, event):
                logger.info(f"Action '{action_name}' executed.")
                return

        except PermissionError as error:
            self._execute("reject_access", event)
            logger.error(f"Access rejected: {error}")

        except Exception as error:
            self._execute("error", event)
            logger.error(error)

        else:
            logger.info("Not a single action was executed.")

    def _execute(self, action_name: str, event: Event) -> ExecResult:
        selected = action_list.get(action_name)
        if selected is None:
            raise ValueError(f"Could not call action '{action_name}'.")

        action_obj = selected(self._get_api())
        return action_obj(event)

    @staticmethod
    def _get_payload(event: Event):
        payload = event.button.payload
        if payload is None:
            raise ValueError("Event does not contains payload.")

        return payload

    @staticmethod
    def _check_owner(payload: Payload, event: Event):
        owner = payload.get("keyboard_owner")
        if owner != event.user.uuid:
            raise PermissionError("The user is not the owner of the message.")

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
