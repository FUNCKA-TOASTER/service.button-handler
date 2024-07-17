from typing import NoReturn, Optional, Any, Union, Dict
from loguru import logger
from vk_api import VkApi
from toaster.broker.events import Event
from actions import action_list
import config


Payload = Dict[str, Union[str, int]]
ExecResult = Optional[Union[bool, NoReturn]]


class ButtonHandler:
    """DOCSTRING"""

    def __call__(self, event: Event) -> None:
        try:
            payload = self.get_payload(event)

            self.check_owner(payload, event)

            action_name = payload.get("call_action")
            if self._execute(action_name):
                logger.info(f"Action '{action_name}' executed.")

        except PermissionError as error:
            self._execute("reject_access")
            logger.error(f"Access rejected: {error}")

        except Exception as error:
            self._execute("error")
            logger.error(error)

    def _execute(self, action_name: str) -> ExecResult:
        selected = action_list.get(action_name)
        if selected is None:
            raise ValueError(f"Could not call action '{action_name}'.")

        action_obj = selected(self._get_api())
        return action_obj()

    @staticmethod
    def get_payload(event: Event):
        payload = event.button.payload
        if payload is None:
            raise ValueError("Event does not contains payload.")

        return payload

    @staticmethod
    def check_owner(payload: Payload, event: Event):
        owner = payload.get("keyboard_owner")
        if owner != event.user.uuid:
            # TODO: fix text
            raise PermissionError("Not message owner")

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
