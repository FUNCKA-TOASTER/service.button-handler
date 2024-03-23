from tools.keyboards import Keyboard
from db import db
import config
from .base import BaseAction



# ------------------------------------------------------------------------
class NotMessageOwnerAction(BaseAction):
    """Action that denies force
    unless it belongs to the author
    of the message with keyboard.
    """
    NAME = "Not Message Owner"

    async def _handle(self, event: dict, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return False



# ------------------------------------------------------------------------
class CancelAction(BaseAction):
    """Cancels the command, closes the menu,
    and deletes the message.
    """
    NAME = "Cancel"

    async def _handle(self, event: dict, kwargs) -> bool:
        self.api.messages.delete(
            peer_id=event.get("peer_id"),
            cmids=event.get("cmid"),
            delete_for_all=1
        )

        snackbar_message = "❗Отмена команды."

        self.snackbar(event, snackbar_message)

        return True

# ------------------------------------------------------------------------
class TestAction(BaseAction):
    """Test action.
    """
    NAME = "TEST"

    async def _handle(self, event: dict, kwargs) -> bool:
        new_msg_text = "Тест был пройден!"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=None)
        )

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json
        )

        snackbar_message = "⚠️ Тест пройден!"

        self.snackbar(event, snackbar_message)

        return True



# ------------------------------------------------------------------------
class MarkAsChatAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    NAME = "Mark as chat"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id")
        )
        already_marked = bool(mark)

        if not already_marked:
            db.execute.insert(
                schema="toaster",
                table="conversations",
                conv_id=event.get("peer_id"),
                conv_name=event.get("peer_name"),
                conv_mark="CHAT"
            )

            snackbar_message = "📝 Беседа помечена как \"чат\"."

        else:
            snackbar_message = f"❗Беседа уже имеет метку \"{mark[0][0]}\"."

        self.snackbar(event, snackbar_message)

        return True



class MarkAsLogAction(BaseAction):
    """Creates a "log" mark and stores
    data about it in the database.
    """
    NAME = "Mark as log"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id")
        )
        already_marked = bool(mark)

        if not already_marked:
            db.execute.insert(
                schema="toaster",
                table="conversations",
                conv_id=event.get("peer_id"),
                conv_name=event.get("peer_name"),
                conv_mark="LOG"
            )

            snackbar_message = "📝 Беседа помечена как \"лог\"."

        else:
            snackbar_message = f"❗Беседа уже имеет метку \"{mark[0][0]}\"."

        self.snackbar(event, snackbar_message)

        return True



class UpdateConvDataAction(BaseAction):
    """Updates the data of a conversation
    that already has a label. First of all,
    it is necessary for the correct display
    of logs when changing the name of the
    conversation.
    """
    NAME = "Update conversation data"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id")
        )
        already_marked = bool(mark)

        if already_marked:
            new_data = {
                "conv_name": event.get("peer_name"),
            }
            db.execute.update(
                schema="toaster",
                table="conversations",
                new_data=new_data,
                conv_id=event.get("peer_id")
            )

            snackbar_message = "📝 Данные беседы обновлены."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True



class DropMarkAction(BaseAction):
    """Removes the mark from the conversation,
    deleting records about it in the database.
    """
    NAME = "Drop conversation mark"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id")
        )
        already_marked = bool(mark)

        if already_marked:
            db.execute.delete(
                schema="toaster",
                table="conversations",
                conv_id=event.get("peer_id")
            )

            snackbar_message = f"📝 Метка \"{mark[0][0]}\" снята с беседы."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True



# ------------------------------------------------------------------------
class SetAdministratorPermissionAction(BaseAction):
    """Sets the user to the "administrator" role,
    records this in the database.
    """
    NAME = "Set administrator permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("user_permission",)
        target_id=event["payload"].get("target")
        lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[2]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if already_promoted:
            lvl = int(lvl[0][0])

            if lvl == 2:
                role = config.PERMISSIONS_DECODING[lvl]
                snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

                self.snackbar(event, snackbar_message)

                return False

        user_name = self.get_name(target_id)

        db.execute.insert(
            schema="toaster",
            table="permissions",
            on_duplicate="update",
            conv_id=event.get("peer_id"),
            user_id=target_id,
            user_name=user_name,
            user_permission=2
        )

        self.snackbar(event, snackbar_message)

        return True


    def get_name(self, user_id: int) -> str:
        """Returns the full name of the user,
        using its unique ID.

        Args:
            user_id (int): User ID.

        Returns:
            str: User full name.
        """
        name = self.api.users.get(
            user_ids=user_id
        )

        if not bool(name):
            name = "Unknown"

        else:
            name = name[0].get("first_name") + \
                " " + name[0].get("last_name")

        return name



class SetModeratorPermissionAction(BaseAction):
    """Sets the user to the "moderator" role,
    records this in the database.
    """
    NAME = "Set moderator permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("user_permission",)
        target_id=event["payload"].get("target")
        lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[1]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if already_promoted:
            lvl = int(lvl[0][0])

            if lvl == 1:
                role = config.PERMISSIONS_DECODING[lvl]
                snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

                self.snackbar(event, snackbar_message)

                return False

        user_name = self.get_name(target_id)

        db.execute.insert(
            schema="toaster",
            table="permissions",
            on_duplicate="update",
            conv_id=event.get("peer_id"),
            user_id=target_id,
            user_name=user_name,
            user_permission=1
        )

        self.snackbar(event, snackbar_message)

        return True


    def get_name(self, user_id: int) -> str:
        """Returns the full name of the user,
        using its unique ID.

        Args:
            user_id (int): User ID.

        Returns:
            str: User full name.
        """
        name = self.api.users.get(
            user_ids=user_id
        )

        if not bool(name):
            name = "Unknown"

        else:
            name = name[0].get("first_name") + \
                " " + name[0].get("last_name")

        return name



class SetUserPermissionAction(BaseAction):
    """Sets the user to the "user" role,
    records this in the database.
    """
    NAME = "Set user permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("user_permission",)
        target_id = event["payload"].get("target")
        lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[0]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if not already_promoted:
            role = config.PERMISSIONS_DECODING[lvl]
            snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

            self.snackbar(event, snackbar_message)

            return False

        db.execute.delete(
            schema="toaster",
            table="permissions",
            user_id=target_id
        )

        self.snackbar(event, snackbar_message)

        return True
