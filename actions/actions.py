from toaster.broker.events import Event
from data import TOASTER_DB
from data.scripts import (
    get_peer_mark,
    set_peer_mark,
)
from .base import BaseAction


# ------------------------------------------------------------------------
class Error(BaseAction):
    NAME = "error"

    def _handle(self, event: Event) -> bool:
        snackbar_message = "⚠️ Что-то пошло не так."
        self.snackbar(event, snackbar_message)

        return False


# ------------------------------------------------------------------------
class RejectAccess(BaseAction):
    NAME = "reject_access"

    def _handle(self, event: Event) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."
        self.snackbar(event, snackbar_message)

        return False


# ------------------------------------------------------------------------
class CloseMenu(BaseAction):
    NAME = "close_menu"

    def _handle(self, event: Event) -> bool:
        self.api.messages.delete(
            peer_id=event.peer.bpid,
            cmids=event.button.cmid,
            delete_for_all=1,
        )

        snackbar_message = "❌ Меню закрыто."
        self.snackbar(event, snackbar_message)

        # TODO: Удаление сессии меню из БД

        return True


# ------------------------------------------------------------------------
class SetMark(BaseAction):
    NAME = "set_mark"

    def _handle(self, event: Event) -> bool:
        mark = get_peer_mark(TOASTER_DB, event.peer.bpid)

        if mark is None:
            payload = event.button.payload
            mark = payload.get("mark")

            set_peer_mark(TOASTER_DB, mark, event)
            snackbar_message = f'📝 Беседа помечена как "{mark}".'

        else:
            snackbar_message = f'❗Беседа уже имеет метку "{mark}".'

        self.snackbar(event, snackbar_message)

        return True
