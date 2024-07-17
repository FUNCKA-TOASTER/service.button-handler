from toaster.broker.events import Event
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

        snackbar_message = "❗Отмена команды."
        self.snackbar(event, snackbar_message)

        # TODO: Удаление сессии меню из БД

        return True


# ------------------------------------------------------------------------
# class SetMark(BaseAction):
#     NAME = "set_mark"

#     def _handle(self, event: Event) -> bool:
#         fields = ("conv_mark",)
#         mark = db.execute.select(
#             schema="toaster",
#             table="conversations",
#             fields=fields,
#             conv_id=event.get("peer_id"),
#         )
#         already_marked = bool(mark)

#         payload = event.get("payload")
#         mark = payload.get("mark")

#         if not already_marked:
#             db.execute.insert(
#                 schema="toaster",
#                 table="conversations",
#                 conv_id=event.get("peer_id"),
#                 conv_name=event.get("peer_name"),
#                 conv_mark=mark,
#             )

#             snackbar_message = f'📝 Беседа помечена как "{mark}".'

#         else:
#             snackbar_message = f'❗Беседа уже имеет метку "{mark}".'

#         self.snackbar(event, snackbar_message)

#         return True
