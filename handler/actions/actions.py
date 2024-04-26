import random
from tools.keyboards import Keyboard, Callback, ButtonColor
from db import db
import config
from .base import BaseAction


# ------------------------------------------------------------------------
class NotMessageOwnerAction(BaseAction):
    NAME = "not_msg_owner"

    async def _handle(self, event: dict, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return False


# ------------------------------------------------------------------------
# TODO: Добавить удаление записи сесси меню из БД
class CancelAction(BaseAction):
    NAME = "cancel_command"

    async def _handle(self, event: dict, kwargs) -> bool:
        self.api.messages.delete(
            peer_id=event.get("peer_id"), cmids=event.get("cmid"), delete_for_all=1
        )

        snackbar_message = "❗Отмена команды. "

        self.snackbar(event, snackbar_message)
        self._close_session(event)

        return True

    def _close_session(self, event):
        db.execute.delete(
            schema="toaster",
            table="menu_sessions",
            conv_id=event.get("peer_id"),
            cm_id=event.get("cmid"),
        )


# ------------------------------------------------------------------------
class MarkAction(BaseAction):
    NAME = "set_mark"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id"),
        )
        already_marked = bool(mark)

        payload = event.get("payload")
        mark = payload.get("mark")

        if not already_marked:
            db.execute.insert(
                schema="toaster",
                table="conversations",
                conv_id=event.get("peer_id"),
                conv_name=event.get("peer_name"),
                conv_mark=mark,
            )

            snackbar_message = f'📝 Беседа помечена как "{mark}".'

        else:
            snackbar_message = f'❗Беседа уже имеет метку "{mark}".'

        self.snackbar(event, snackbar_message)

        return True


class UpdateConvDataAction(BaseAction):
    NAME = "update_conv_data"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id"),
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
                conv_id=event.get("peer_id"),
            )

            snackbar_message = "📝 Данные беседы обновлены."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


class DropMarkAction(BaseAction):
    NAME = "drop_mark"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=fields,
            conv_id=event.get("peer_id"),
        )
        already_marked = bool(mark)

        if already_marked:
            db.execute.delete(
                schema="toaster", table="conversations", conv_id=event.get("peer_id")
            )

            snackbar_message = f'📝 Метка "{mark[0][0]}" снята с беседы.'

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class SetPermissionAction(BaseAction):
    NAME = "set_permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("user_permission",)
        target_id = event["payload"].get("target")
        lvl = db.execute.select(
            schema="toaster", table="permissions", fields=fields, user_id=target_id
        )
        already_promoted = bool(lvl)
        user_lvl = int(event.get("payload").get("permission"))
        role = config.PERMISSIONS_DECODING[user_lvl]

        if already_promoted:
            if user_lvl == int(lvl[0][0]):
                snackbar_message = f'❗Пользователь уже имеет роль "{role}".'
                self.snackbar(event, snackbar_message)
                return False

            if user_lvl == 0:
                db.execute.delete(
                    schema="toaster", table="permissions", user_id=target_id
                )

                snackbar_message = f'⚒️ Пользователю назначена роль "{role}".'
                self.snackbar(event, snackbar_message)
                return True

        if user_lvl == 0:
            snackbar_message = f'❗Пользователь уже имеет роль "{role}".'
            self.snackbar(event, snackbar_message)
            return False

        snackbar_message = f'⚒️ Пользователю назначена роль "{role}".'

        user_name = self.get_name(target_id)

        db.execute.insert(
            schema="toaster",
            table="permissions",
            on_duplicate="update",
            conv_id=event.get("peer_id"),
            user_id=target_id,
            user_name=user_name,
            user_permission=user_lvl,
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
        name = self.api.users.get(user_ids=user_id)

        if not bool(name):
            name = "Unknown"

        else:
            name = name[0].get("first_name") + " " + name[0].get("last_name")

        return name


class DropPermissionAction(BaseAction):
    NAME = "drop_permission"

    async def _handle(self, event: dict, kwargs) -> bool:
        fields = ("user_permission",)
        target_id = event["payload"].get("target")
        lvl = db.execute.select(
            schema="toaster", table="permissions", fields=fields, user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[0]
        snackbar_message = f'⚒️ Пользователю назначена роль "{role}".'

        if not already_promoted:
            lvl = 0
            role = config.PERMISSIONS_DECODING[lvl]
            snackbar_message = f'❗Пользователь уже имеет роль "{role}".'

            self.snackbar(event, snackbar_message)

            return False

        db.execute.delete(schema="toaster", table="permissions", user_id=target_id)

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class GameRollAction(BaseAction):
    NAME = "game_roll"
    EMOJI = ["0️⃣", "1️⃣", " 2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

    async def _handle(self, event: dict, kwargs) -> bool:
        result = random.randint(0, 100)
        result = self._convert_to_emoji(result)

        tag = f"[id{event.get('user_id')}|{event.get('user_name')}]"

        new_msg_text = f"{tag} выбивает число: {result}"

        keyboard = Keyboard(inline=True, one_time=False, owner_id=None)

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        snackbar_message = "🎲 Рулетка прокручена!"

        self.snackbar(event, snackbar_message)

        return True

    def _convert_to_emoji(self, number):
        result = ""

        for didgit in str(number):
            result += self.EMOJI[int(didgit)]

        return result


class GameCoinflipAction(BaseAction):
    NAME = "game_coinflip"
    EMOJI = ["Орёл 🪙", "Решка 🪙"]

    async def _handle(self, event: dict, kwargs) -> bool:
        result = random.randint(0, 1)
        result = self._convert_to_emoji(result)

        tag = f"[id{event.get('user_id')}|{event.get('user_name')}]"

        new_msg_text = f"{tag} подбрасывает монетку: {result}"

        keyboard = Keyboard(inline=True, one_time=False, owner_id=None)

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        snackbar_message = "🎲 Монета брошена!"

        self.snackbar(event, snackbar_message)

        return True

    def _convert_to_emoji(self, number):
        return self.EMOJI[number]


# ------------------------------------------------------------------------
class SystemsSettingsAction(BaseAction):
    NAME = "systems_settings"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        systems = db.execute.select(
            schema="toaster_settings",
            table="settings",
            fields=("setting_name", "setting_status"),
            conv_id=event.get("peer_id"),
            setting_destination="system",
        )

        sys_status = {row[0]: int(row[1]) for row in systems}

        color_by_status = {0: ButtonColor.NEGATIVE, 1: ButtonColor.POSITIVE}

        page = int(payload.get("page", 1))

        if payload.get("sub_action") == "change_setting":
            sys_name = payload.get("system_name")
            new_status = abs(sys_status[sys_name] - 1)  # (0 to 1) or (1 to 0)
            sys_status[sys_name] = new_status
            snackbar_message = f"⚠️ Система {'Включена' if new_status else 'Выключена'}."
            db.execute.update(
                schema="toaster_settings",
                table="settings",
                new_data={"setting_status": new_status},
                conv_id=event.get("peer_id"),
                setting_name=sys_name,
                setting_destination="system",
            )

        else:
            snackbar_message = f"⚙️ Меню систем модерации ({page}/2).."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Возраст аккаунта: {'Вкл.' if sys_status['account_age'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "account_age",
                            "page": "1",
                        },
                    ),
                    color_by_status[sys_status["account_age"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Запрещенные слова: {'Вкл.' if sys_status['curse_words'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "curse_words",
                            "page": "1",
                        },
                    ),
                    color_by_status[sys_status["curse_words"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Открытое ЛС: {'Вкл.' if sys_status['open_pm'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "open_pm",
                            "page": "1",
                        },
                    ),
                    color_by_status[sys_status["open_pm"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Медленный режим: {'Вкл.' if sys_status['slow_mode'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "slow_mode",
                            "page": "1",
                        },
                    ),
                    color_by_status[sys_status["slow_mode"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "systems_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        if page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Фильтрация URL: {'Вкл.' if sys_status['url_filtering'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "url_filtering",
                            "page": "2",
                        },
                    ),
                    color_by_status[sys_status["url_filtering"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Усиленная фильтрация URL: {'Вкл.' if sys_status['hard_url_filtering'] else 'Выкл.'}",
                        payload={
                            "call_action": "systems_settings",
                            "sub_action": "change_setting",
                            "system_name": "hard_url_filtering",
                            "page": "2",
                        },
                    ),
                    color_by_status[sys_status["hard_url_filtering"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "systems_settings", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Включение\\Выключение систем модерации:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


class FiltersSettingsAction(BaseAction):
    NAME = "filters_settings"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        systems = db.execute.select(
            schema="toaster_settings",
            table="settings",
            fields=("setting_name", "setting_status"),
            conv_id=event.get("peer_id"),
            setting_destination="filter",
        )

        filt_status = {row[0]: int(row[1]) for row in systems}

        color_by_status = {0: ButtonColor.NEGATIVE, 1: ButtonColor.POSITIVE}

        page = int(payload.get("page", 1))

        if payload.get("sub_action") == "change_setting":
            filt_name = payload.get("filter_name")
            new_status = abs(filt_status[filt_name] - 1)  # (0 to 1) or (1 to 0)
            filt_status[filt_name] = new_status
            snackbar_message = (
                f"⚠️ Фильтр {'Включен' if not new_status else 'Выключен'}."
            )
            db.execute.update(
                schema="toaster_settings",
                table="settings",
                new_data={"setting_status": new_status},
                conv_id=event.get("peer_id"),
                setting_name=filt_name,
                setting_destination="filter",
            )

        else:
            snackbar_message = f"⚙️ Меню фильтров сообщений ({page}/4)."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Приложения: {'Выкл.' if filt_status['app_action'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "app_action",
                            "page": "1",
                        },
                    ),
                    color_by_status[filt_status["app_action"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Музыка: {'Выкл.' if filt_status['audio'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "audio",
                            "page": "1",
                        },
                    ),
                    color_by_status[filt_status["audio"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Аудио: {'Выкл.' if filt_status['audio_message'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "audio_message",
                            "page": "1",
                        },
                    ),
                    color_by_status[filt_status["audio_message"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Файлы: {'Выкл.' if filt_status['doc'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "doc",
                            "page": "1",
                        },
                    ),
                    color_by_status[filt_status["doc"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Пересыл: {'Выкл.' if filt_status['forward'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "forward",
                            "page": "2",
                        },
                    ),
                    color_by_status[filt_status["forward"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Ответ: {'Выкл.' if filt_status['reply'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "reply",
                            "page": "2",
                        },
                    ),
                    color_by_status[filt_status["reply"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Граффити: {'Выкл.' if filt_status['graffiti'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "graffiti",
                            "page": "2",
                        },
                    ),
                    color_by_status[filt_status["graffiti"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Стикеры: {'Выкл.' if filt_status['sticker'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "sticker",
                            "page": "2",
                        },
                    ),
                    color_by_status[filt_status["sticker"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_settings", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_settings", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 3:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Линки: {'Выкл.' if filt_status['link'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "link",
                            "page": "3",
                        },
                    ),
                    color_by_status[filt_status["link"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Изображения: {'Выкл.' if filt_status['photo'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "photo",
                            "page": "3",
                        },
                    ),
                    color_by_status[filt_status["photo"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Опросы: {'Выкл.' if filt_status['poll'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "poll",
                            "page": "3",
                        },
                    ),
                    color_by_status[filt_status["poll"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Видео: {'Выкл.' if filt_status['video'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "video",
                            "page": "3",
                        },
                    ),
                    color_by_status[filt_status["video"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_settings", "page": "4"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 4:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label=f"Записи: {'Выкл.' if filt_status['Wall'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "wall",
                            "page": "4",
                        },
                    ),
                    color_by_status[filt_status["Wall"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Геопозиция: {'Выкл.' if filt_status['geo'] else 'Вкл.'}",
                        payload={
                            "call_action": "filters_settings",
                            "sub_action": "change_setting",
                            "filter_name": "geo",
                            "page": "4",
                        },
                    ),
                    color_by_status[filt_status["geo"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_settings", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Включение\\Выключение фильтров сообщений:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class ChangeDelayAction(BaseAction):
    NAME = "change_delay"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]
        setting = payload.get("setting")

        delay = db.execute.select(
            schema="toaster_settings",
            table="delay",
            fields=("delay",),
            conv_id=event.get("peer_id"),
            setting_name=setting,
        )

        delay = int(delay[0][0])
        sub_action = payload.get("sub_action")

        if sub_action is not None:
            time = payload.get("time")

            if sub_action == "subtract_time":
                delay = (delay - time) if (delay - time) > 0 else 0
                snackbar_message = "⚠️ Время уменьшено."

            elif sub_action == "add_time":
                delay = delay + time
                snackbar_message = "⚠️ Время увеличено."

            db.execute.update(
                schema="toaster_settings",
                table="delay",
                new_data={"delay": delay},
                conv_id=event.get("peer_id"),
                setting_name=setting,
            )

        else:
            snackbar_message = "⚙️ Меню установки задержки."

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="- 1",
                    payload={
                        "call_action": "change_delay",
                        "sub_action": "subtract_time",
                        "time": 1,
                        "setting": setting,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 1",
                    payload={
                        "call_action": "change_delay",
                        "sub_action": "add_time",
                        "time": 1,
                        "setting": setting,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="- 10",
                    payload={
                        "call_action": "change_delay",
                        "sub_action": "subtract_time",
                        "time": 10,
                        "setting": setting,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 10",
                    payload={
                        "call_action": "change_delay",
                        "sub_action": "add_time",
                        "time": 10,
                        "setting": setting,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Закрыть меню", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.SECONDARY,
            )
        )

        if setting == "slow_mode":
            new_msg_text = (
                "⚙️ Задержка для данного чата установлена на "
                f"{delay} {self._get_min_declension(delay)}."
            )
        elif setting == "account_age":
            new_msg_text = (
                "⚙️ Критерий новизны аккаунта для данного чата установлен на "
                f"{delay} {self._get_day_declension(delay)}."
            )

        elif setting == "menu_session":
            new_msg_text = (
                "⚙️ Время жизни сесси меню установлена на: "
                f"{delay} {self._get_min_declension(delay)}."
            )

        elif setting == "red_zone":
            new_msg_text = (
                "⚙️ Время истечения срока наказания для красной зоны выставлен на: "
                f"{delay} {self._get_day_declension(delay)}."
            )

        elif setting == "yellow_zone":
            new_msg_text = (
                "⚙️ Время истечения срока наказания для жёлтой зоны выставлен на: "
                f"{delay} {self._get_day_declension(delay)}."
            )
        elif setting == "green_zone":
            new_msg_text = (
                "⚙️ Время истечения срока наказания для зелёной зоны выставлен на: "
                f"{delay} {self._get_day_declension(delay)}."
            )

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True

    @staticmethod
    def _get_min_declension(minutes: int) -> str:
        timename = "минут"
        if 11 <= minutes and minutes <= 14:
            timename = "минут"

        elif minutes % 10 == 1:
            timename = "минуту"

        elif 2 <= (minutes % 10) and (minutes % 10) <= 4:
            timename = "минуты"

        return timename

    @staticmethod
    def _get_day_declension(minutes: int) -> str:
        timename = "дней"
        if 11 <= minutes and minutes <= 14:
            timename = "дней"

        elif minutes % 10 == 1:
            timename = "день"

        elif 2 <= (minutes % 10) and (minutes % 10) <= 4:
            timename = "дня"

        return timename


# ------------------------------------------------------------------------
class SystemsPunishmentAction(BaseAction):
    NAME = "systems_punishment"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        page = int(payload.get("page", 1))
        snackbar_message = f"⚙️ Меню систем модерации ({page}/2).."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Возраст аккаунта",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "account_age",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Запрещенные слова",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "curse_words",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Открытое ЛС",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "open_pm",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Медленный режим",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "slow_mode",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "systems_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        if page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Фильтрация URL",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "url_filtering",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Усиленная фильтрация URL",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "hard_url_filtering",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "systems_punishment", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Выберете необходимую систему:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


class FiltersPunishmentAction(BaseAction):
    NAME = "filters_punishment"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]

        page = int(payload.get("page", 1))
        snackbar_message = f"⚙️ Меню фильтров сообщений ({page}/4)."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Приложения",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "app_action",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Музыка",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "audio",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Аудио",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "audio_message",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Файлы",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "doc",
                            "page": "1",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Пересыл",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "forward",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Ответ",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "reply",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Граффити",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "graffiti",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Стикеры",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "sticker",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_punishment", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_punishment", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 3:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Линки",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "link",
                            "page": "3",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Изображения",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "photo",
                            "page": "3",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Опросы",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "poll",
                            "page": "3",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Видео",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "video",
                            "page": "3",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"call_action": "filters_punishment", "page": "4"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 4:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
                .add_row()
                .add_button(
                    Callback(
                        label="Записи",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "wall",
                            "page": "4",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Геопозиция",
                        payload={
                            "call_action": "change_punishment",
                            "setting_name": "geo",
                            "page": "4",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"call_action": "filters_punishment", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="Закрыть меню", payload={"call_action": "cancel_command"}
                    ),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Выберете необходимый фильтр:"
        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


class ChangePunishmentAction(BaseAction):
    NAME = "change_punishment"

    async def _handle(self, event: dict, kwargs) -> bool:
        payload = event["payload"]
        setting = payload.get("setting_name")

        warns = db.execute.select(
            schema="toaster_settings",
            table="settings",
            fields=("warn_point",),
            conv_id=event.get("peer_id"),
            setting_name=setting,
        )

        warns = int(warns[0][0])
        sub_action = payload.get("sub_action")

        if sub_action is not None:
            points = payload.get("points")

            if sub_action == "subtract_points":
                warns = (warns - points) if (warns - points) > 0 else 0
                snackbar_message = "⚠️ Наказание уменьшено."

            elif sub_action == "add_points":
                warns = (warns + points) if (warns + points) <= 10 else 10
                snackbar_message = "⚠️ Наказание увеличено."

            db.execute.update(
                schema="toaster_settings",
                table="settings",
                new_data={"warn_point": warns},
                conv_id=event.get("peer_id"),
                setting_name=setting,
            )

        else:
            snackbar_message = "⚙️ Меню установки наказания."

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("user_id"))
            .add_row()
            .add_button(
                Callback(
                    label="- 1 пред.",
                    payload={
                        "call_action": "change_punishment",
                        "setting_name": setting,
                        "sub_action": "subtract_points",
                        "points": 1,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 1 пред.",
                    payload={
                        "call_action": "change_punishment",
                        "setting_name": setting,
                        "sub_action": "add_points",
                        "points": 1,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="- 3 пред.",
                    payload={
                        "call_action": "change_punishment",
                        "setting_name": setting,
                        "sub_action": "subtract_points",
                        "points": 3,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 3 пред.",
                    payload={
                        "call_action": "change_punishment",
                        "setting_name": setting,
                        "sub_action": "add_points",
                        "points": 3,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="Закрыть меню", payload={"call_action": "cancel_command"}
                ),
                ButtonColor.SECONDARY,
            )
        )

        new_msg_text = (
            f"⚙️ Наказание для настройки {setting} установлено на: "
            f"{warns} {self._get_warn_declension(warns)}."
        )

        self.api.messages.edit(
            peer_id=event.get("peer_id"),
            conversation_message_id=event.get("cmid"),
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True

    @staticmethod
    def _get_warn_declension(minutes: int) -> str:
        timename = "предупреждений"
        if 11 <= minutes and minutes <= 14:
            timename = "предупреждений"

        elif minutes % 10 == 1:
            timename = "предупреждение"

        elif 2 <= (minutes % 10) and (minutes % 10) <= 4:
            timename = "предупреждения"

        return timename
