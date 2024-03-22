from .base import BaseAction



# ------------------------------------------------------------------------
class NotMessageOwnerAction(BaseAction):
    """Action that denies force
    unless it belongs to the author
    of the message with keyboard.
    """
    async def _handle(self, event: dict, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return False



# ------------------------------------------------------------------------
class CancelAction(BaseAction):
    """Cancels the command, closes the menu,
    and deletes the message.
    """
    async def _handle(self, event: dict, kwargs) -> bool:
        self.api.messages.delete(
            peer_id=event.get("peer_id"),
            cmids=event.get("cmid"),
            delete_for_all=1
        )

        snackbar_message = "❗Отмена команды."

        self.snackbar(event, snackbar_message)

        return True
