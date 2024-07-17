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

            self.check_owner(payload)

            action_name = payload.get("call_action")
            if self._execute(action_name, event):
                logger.info(f"Action '{action_name}' executed.")

        except Exception as error:
            logger.error(error)

    def _execute(self, action_name: str, event: Event) -> ExecResult:
        selected = action_list.get(action_name)
        if selected is None:
            # TODO: fix exeption
            raise Exception(f"Could not call action '{action_name}'.")

        action_obj = selected(self._get_api())
        return action_obj()

    @staticmethod
    def get_payload(event: Event):
        payload = event.get("payload")
        if payload is None:
            raise ValueError("Event does not contains payload.")

        return payload

    @staticmethod
    def check_owner(payload: Payload, event: Event):
        owner = payload.get("keyboard_owner")
        if owner != event.user.uuid:
            # TODO: call  not_msg_owner action
            # TODO: fix text and exeption
            raise Exception("Not message owner")

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
