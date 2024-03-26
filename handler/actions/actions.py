import random
from tools.keyboards import (
    Keyboard,
    Callback,
    ButtonColor
)
from db import db
import config
from .base import BaseAction


# ------------------------------------------------------------------------
class NotMessageOwnerAction(BaseAction):
    """Action that denies force
    unless it belongs to the author
    of the message with keyboard.
    """
    NAME = "not_msg_owner"

    async def _handle(self, event: dict, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return False



# ------------------------------------------------------------------------
class CancelAction(BaseAction):
    """Cancels the command, closes the menu,
    and deletes the message.
    """
    NAME = "cancel_command"

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
class MarkAsChatAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    NAME = "mark_as_chat"

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

            snackbar_message = "📝 Беседа помечена как \"CHAT\"."

        else:
            snackbar_message = f"❗Беседа уже имеет метку \"{mark[0][0]}\"."

        self.snackbar(event, snackbar_message)

        return True



class MarkAsLogAction(BaseAction):
    """Creates a "log" mark and stores
    data about it in the database.
    """
    NAME = "mark_as_log"

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

            snackbar_message = "📝 Беседа помечена как \"LOG\"."

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
    NAME = "update_conv_data"

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
    NAME = "drop_mark"

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
    NAME = "set_administrator_permission"

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
    NAME = "set_moderator_permission"

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
    NAME = "set_user_permission"

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



# ------------------------------------------------------------------------
class GameRollAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    NAME = "game_roll"
    EMOJI=['0️⃣', '1️⃣',' 2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣' ,'8️⃣', '9️⃣']

    async def _handle(self, event: dict, kwargs) -> bool:
        result = random.randint(0,100)
        result = self._convert_to_emoji(result)

        tag = f"[id{event.get('user_id')}|{event.get('user_name')}]"

        new_msg_text = f"{tag} выбивает число: {result}"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=None)
        )

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json
        )

        snackbar_message = "🎲 Рулетка прокручена!"

        self.snackbar(event, snackbar_message)

        return True


    def _convert_to_emoji(self, number):
        result = ''

        for didgit in str(number):
            result += self.EMOJI[int(didgit)]

        return result


class GameCoinflipAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    NAME = "game_coinflip"
    EMOJI = ["Орёл 🪙", "Решка 🪙"]

    async def _handle(self, event: dict, kwargs) -> bool:
        result = random.randint(0, 1)
        result = self._convert_to_emoji(result)

        tag = f"[id{event.get('user_id')}|{event.get('user_name')}]"

        new_msg_text = f"{tag} подбрасывает монетку: {result}"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=None)
        )

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json
        )

        snackbar_message = "🎲 Монета брошена!"

        self.snackbar(event, snackbar_message)

        return True


    def _convert_to_emoji(self, number):
        return self.EMOJI[number]


# ------------------------------------------------------------------------
class SystemSettingsPageOneAction(BaseAction):
    NAME = "systems_settings_page_1"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        systems = db.execute.select(
            schema="toaster_settings",
            table="system_status",
            fields=("system_name", "system_status"),
            conv_id=event.get("peer_id")
        )

        sys_status = {
            row[0]: int(row[1]) for row in systems
        }

        color_by_status = {
            0: ButtonColor.NEGATIVE,    
            1: ButtonColor.POSITIVE
        }

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=None)
            .add_row()
            .add_button(
                Callback(
                    label=f"Возраста аккаунта: {'Вкл.' if sys_status['Account_age'] else 'Выкл.'}",
                    payload={
                        "call_action": "system_settings_page_1",
                        "sub_action": "change_setting",
                        "system_name": "Account_age"
                    }
                ),
                color_by_status[sys_status["Account_age"]]
            )
            .add_row()
            .add_button(
                Callback(
                    label=f"Плохие слова: {'Вкл.' if sys_status['Curse_words'] else 'Выкл.'}",
                    payload={
                        "call_action": "system_settings_page_1",
                        "sub_action": "change_setting",
                        "system_name": "Curse_words"
                    }
                ),
                color_by_status[sys_status["Curse_words"]]
            )
            .add_row()
            .add_button(
                Callback(
                    label=f"Усиленый режим: {'Вкл.' if sys_status['Hard_mode'] else 'Выкл.'}",
                    payload={
                        "call_action": "system_settings_page_1",
                        "sub_action": "change_setting",
                        "system_name": "Hard_mode"
                    }
                ),
                color_by_status[sys_status["Hard_mode"]]
            )
            .add_row()
            .add_button(
                Callback(
                    label=f"Открытое ЛС: {'Вкл.' if sys_status['Open_pm'] else 'Выкл.'}",
                    payload={
                        "call_action": "system_settings_page_1",
                        "sub_action": "change_setting",
                        "system_name": "Open_pm"
                    }
                ),
                color_by_status[sys_status["Open_pm"]]
            )
            .add_row()
            .add_button(
                Callback(
                    label=f"Медленный режим: {'Вкл.' if sys_status['Slow_mode'] else 'Выкл.'}",
                    payload={
                        "call_action": "system_settings_page_1",
                        "sub_action": "change_setting",
                        "system_name": "Slow_mode"
                    }
                ),
                color_by_status[sys_status["Slow_mode"]]
            )
            .add_row()
            .add_button(
                Callback(
                    label="Закрыть меню",
                    payload={
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.SECONDARY
            )
        )

        new_msg_text = "⚙️ Влючение\\Выключение систем модерации:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json
        )

        if payload.get("sub_action") == "change_setting":
            sys_name = payload.get("system_name")
            new_status = abs(sys_status[sys_name] - 1) # (0 to 1) or (1 to 0)
            snackbar_message = f"⚠️ Система {'Влючена' if new_status else 'Выключена'}."
            db.execute.update(
                schema="toaster_settings",
                table="system_status",
                new_data={"system_status": new_status},
                conv_id=event.get("peer_id")
            )

        else:
            snackbar_message = "⚙️ Меню систем модерации."

        self.snackbar(event, snackbar_message)

        return True



class FilterSettingsPageOneAction(BaseAction):
    NAME = "filter_settings_page_1"

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
