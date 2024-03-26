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
class SystemSettingsAction(BaseAction):
    NAME = "systems_settings"

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

        if payload.get("sub_action") == "change_setting":
            sys_name = payload.get("system_name")
            new_status = abs(sys_status[sys_name] - 1) # (0 to 1) or (1 to 0)
            sys_status[sys_name] = new_status
            snackbar_message = f"⚠️ Система {'Влючена' if new_status else 'Выключена'}."
            db.execute.update(
                schema="toaster_settings",
                table="system_status",
                new_data={"system_status": new_status},
                conv_id=event.get("peer_id"),
                system_name=sys_name
            )

        else:
            snackbar_message = "⚙️ Меню систем модерации."

        page = int(payload.get("page", 1))
        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Возраста аккаунта: {'Вкл.' if sys_status['Account_age'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings_page_1",
                            "sub_action": "change_setting",
                            "system_name": "Account_age",
                            "page": "1"
                        }
                    ),
                    color_by_status[sys_status["Account_age"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Плохие слова: {'Вкл.' if sys_status['Curse_words'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings_page_1",
                            "sub_action": "change_setting",
                            "system_name": "Curse_words",
                            "page": "1"
                        }
                    ),
                    color_by_status[sys_status["Curse_words"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Усиленый режим: {'Вкл.' if sys_status['Hard_mode'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings_page_1",
                            "sub_action": "change_setting",
                            "system_name": "Hard_mode",
                            "page": "1"
                        }
                    ),
                    color_by_status[sys_status["Hard_mode"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Открытое ЛС: {'Вкл.' if sys_status['Open_pm'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings_page_1",
                            "sub_action": "change_setting",
                            "system_name": "Open_pm",
                            "page": "1"
                        }
                    ),
                    color_by_status[sys_status["Open_pm"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Медленный режим: {'Вкл.' if sys_status['Slow_mode'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings_page_1",
                            "sub_action": "change_setting",
                            "system_name": "Slow_mode",
                            "page": "1"
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

        self.snackbar(event, snackbar_message)

        return True



class FilterSettingsAction(BaseAction):
    NAME = "filters_settings"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        systems = db.execute.select(
            schema="toaster_settings",
            table="filter_status",
            fields=("filter_name", "filter_status"),
            conv_id=event.get("peer_id")
        )

        filt_status = {
            row[0]: int(row[1]) for row in systems
        }

        color_by_status = {
            0: ButtonColor.NEGATIVE,
            1: ButtonColor.POSITIVE
        }

        if payload.get("sub_action") == "change_setting":
            filt_name = payload.get("filter_name")
            new_status = abs(filt_status[filt_name] - 1) # (0 to 1) or (1 to 0)
            filt_status[filt_name] = new_status
            snackbar_message = f"⚠️ Фильтр {'Влючен' if new_status else 'Выключен'}."
            db.execute.update(
                schema="toaster_settings",
                table="filter_status",
                new_data={"filter_status": new_status},
                conv_id=event.get("peer_id"),
                system_name=filt_name
            )

        else:
            snackbar_message = "⚙️ Меню фильтров сообщений."

        page = int(payload.get("page", 1))
        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Приложения: {'Вкл.' if filt_status['App_action'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "App_action",
                            "page": "1"
                        }
                    ),
                    color_by_status[filt_status["App_action"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Музыка: {'Вкл.' if filt_status['Audio'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Audio",
                            "page": "1"
                        }
                    ),
                    color_by_status[filt_status["Audio"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Аудио: {'Вкл.' if filt_status['Audio_message'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Audio_message",
                            "page": "1"
                        }
                    ),
                    color_by_status[filt_status["Audio_message"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Файлы: {'Вкл.' if filt_status['Doc'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Doc",
                            "page": "1"
                        }
                    ),
                    color_by_status[filt_status["Doc"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={
                            "call_action": "filters_settings",
                            "page": "2"
                        }
                    ),
                    ButtonColor.SECONDARY
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

        elif page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Пересыл: {'Вкл.' if filt_status['Forward'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "Forward",
                            "page": "2"
                        }
                    ),
                    color_by_status[filt_status["Forward"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Ответ: {'Вкл.' if filt_status['Reply'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Reply",
                            "page": "2"
                        }
                    ),
                    color_by_status[filt_status["Reply"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Граффити: {'Вкл.' if filt_status['Graffiti'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Graffiti",
                            "page": "2"
                        }
                    ),
                    color_by_status[filt_status["Graffiti"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Стикеры: {'Вкл.' if filt_status['Sticker'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Sticker",
                            "page": "2"
                        }
                    ),
                    color_by_status[filt_status["Sticker"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={
                            "call_action": "filters_settings",
                            "page": "1"
                        }
                    ),
                    ButtonColor.SECONDARY
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={
                            "call_action": "filters_settings",
                            "page": "3"
                        }
                    ),
                    ButtonColor.SECONDARY
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

        elif page == 3:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Линки: {'Вкл.' if filt_status['Link'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "Link",
                            "page": "3"
                        }
                    ),
                    color_by_status[filt_status["Link"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Изображения: {'Вкл.' if filt_status['Photo'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Photo",
                            "page": "3"
                        }
                    ),
                    color_by_status[filt_status["Photo"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Опросы: {'Вкл.' if filt_status['Poll'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Poll",
                            "page": "3"
                        }
                    ),
                    color_by_status[filt_status["Poll"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Видео: {'Вкл.' if filt_status['Video'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "system_name": "Video",
                            "page": "3"
                        }
                    ),
                    color_by_status[filt_status["Video"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={
                            "call_action": "filters_settings",
                            "page": "2"
                        }
                    ),
                    ButtonColor.SECONDARY
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={
                            "call_action": "filters_settings",
                            "page": "4"
                        }
                    ),
                    ButtonColor.SECONDARY
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

        elif page == 4:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Записи: {'Вкл.' if filt_status['Wall'] else 'Выкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "Wall",
                            "page": "4"
                        }
                    ),
                    color_by_status[filt_status["Wall"]]
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={
                            "call_action": "filters_settings",
                            "page": "3"
                        }
                    ),
                    ButtonColor.SECONDARY
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

        new_msg_text = "⚙️ Влючение\\Выключение фильтров сообщений:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json
        )

        self.snackbar(event, snackbar_message)

        return True
