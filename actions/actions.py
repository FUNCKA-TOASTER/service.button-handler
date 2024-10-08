"""Module "actions".

File:
    actions.py

About:
    File describing possible button response actions.
"""

import random
from funcka_bots.events import BaseEvent
from funcka_bots.keyboards import Keyboard, ButtonColor, Callback
from toaster.enums import (
    UserPermission,
    SettingDestination,
    SettingStatus,
    PeerMark,
)
from toaster.scripts import (
    get_peer_mark,
    set_peer_mark,
    drop_peer_mark,
    update_peer_data,
    get_user_permission,
    set_user_permission,
    drop_user_permission,
    get_destinated_settings_status,
    update_setting_status,
    get_setting_points,
    update_setting_points,
    get_setting_delay,
    update_setting_delay,
    close_menu_session,
)
from .base import BaseAction


# ------------------------------------------------------------------------
class Error(BaseAction):
    NAME = "error"

    def _handle(self, event: BaseEvent) -> bool:
        snackbar_message = "⚠️ Что-то пошло не так."
        self.snackbar(event, snackbar_message)

        return False


class RejectAccess(BaseAction):
    NAME = "reject_access"

    def _handle(self, event: BaseEvent) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."
        self.snackbar(event, snackbar_message)

        return False


class CloseMenu(BaseAction):
    NAME = "close_menu"

    def _handle(self, event: BaseEvent) -> bool:
        self.api.messages.delete(
            peer_id=event.peer.bpid,
            cmids=event.button.cmid,
            delete_for_all=1,
        )

        snackbar_message = "❌ Меню закрыто."
        self.snackbar(event, snackbar_message)

        close_menu_session(bpid=event.peer.bpid, cmid=event.button.cmid)

        return True


# ------------------------------------------------------------------------
class SetMark(BaseAction):
    NAME = "set_mark"

    def _handle(self, event: BaseEvent) -> bool:
        mark = get_peer_mark(bpid=event.peer.bpid)

        if mark is None:
            payload = event.button.payload
            mark = PeerMark(payload.get("mark"))

            set_peer_mark(mark=mark, bpid=event.peer.bpid, name=event.peer.name)
            snackbar_message = f'📝 Беседа помечена как "{mark.name}".'

        else:
            snackbar_message = f'❗Беседа уже имеет метку "{mark.name}".'

        self.snackbar(event, snackbar_message)

        return True


class UpdatePeerData(BaseAction):
    NAME = "update_peer_data"

    def _handle(self, event: BaseEvent) -> bool:
        mark = get_peer_mark(bpid=event.peer.bpid)

        if mark is not None:
            update_peer_data(bpid=event.peer.bpid, name=event.peer.name)
            snackbar_message = "📝 Данные беседы обновлены."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


class DropMark(BaseAction):
    NAME = "drop_mark"

    def _handle(self, event: BaseEvent) -> bool:
        mark = get_peer_mark(bpid=event.peer.bpid)

        if mark is not None:
            drop_peer_mark(bpid=event.peer.bpid)
            snackbar_message = f'📝 Метка "{mark.name}" снята с беседы.'

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class SetPermission(BaseAction):
    NAME = "set_permission"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        target_uuid = payload.get("target")

        current_permission = get_user_permission(uuid=target_uuid, bpid=event.peer.bpid)
        new_permission = UserPermission(int(payload.get("permission")))

        if current_permission == UserPermission.user:
            set_user_permission(
                uuid=target_uuid, bpid=event.peer.bpid, lvl=new_permission
            )
            snackbar_message = f'⚒️ Пользователю назначена роль "{new_permission.name}".'
            self.snackbar(event, snackbar_message)
            return True

        else:
            snackbar_message = (
                f'❗Пользователь уже имеет роль "{current_permission.name}".'
            )
            self.snackbar(event, snackbar_message)
            return False


class DropPermission(BaseAction):
    NAME = "drop_permission"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        target_uuid = payload.get("target")

        current_permission = get_user_permission(
            uuid=target_uuid, bpid=event.peer.bpid, ignore_staff=True
        )

        if current_permission != UserPermission.user:
            drop_user_permission(uuid=target_uuid, bpid=event.peer.bpid)
            snackbar_message = "⚒️ Роль пользователя сброшена."
            self.snackbar(event, snackbar_message)
            return True

        else:
            snackbar_message = "❗ Пользователь не имеет роли."
            self.snackbar(event, snackbar_message)
            return False


# ------------------------------------------------------------------------
class GameRoll(BaseAction):
    NAME = "game_roll"
    EMOJI = ["0️⃣", "1️⃣", " 2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

    def _handle(self, event: BaseEvent) -> bool:
        num = random.randint(0, 100)
        result = ""
        for didgit in str(num):
            result += self.EMOJI[int(didgit)]

        tag = f"[id{event.user.uuid}|{event.user.name}]"
        new_msg_text = f"{tag} выбивает число: {result}"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(label="Скрыть", payload={"action_name": "close_menu"}),
                ButtonColor.SECONDARY,
            )
        )

        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        snackbar_message = "🎲 Рулетка прокручена!"
        self.snackbar(event, snackbar_message)

        return True


class GameCoinflip(BaseAction):
    NAME = "game_coinflip"
    EMOJI = ["Орёл 🪙", "Решка 🪙"]

    def _handle(self, event: BaseEvent) -> bool:
        num = random.randint(0, 1)
        result = self.EMOJI[num]

        tag = f"[id{event.user.uuid}|{event.user.name}]"
        new_msg_text = f"{tag} подбрасывает монетку: {result}"

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(label="Скрыть", payload={"action_name": "close_menu"}),
                ButtonColor.SECONDARY,
            )
        )

        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        snackbar_message = "🎲 Монета брошена!"
        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class SystemsSettings(BaseAction):
    NAME = "systems_settings"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload

        systems = get_destinated_settings_status(
            destination=SettingDestination.system, bpid=event.peer.bpid
        )
        color_by_status = {
            SettingStatus.inactive: ButtonColor.NEGATIVE,
            SettingStatus.active: ButtonColor.POSITIVE,
        }

        page = int(payload.get("page", 1))

        if payload.get("action_context") == "change_status":
            system_name = payload.get("system_name")
            new_status = SettingStatus(not systems[system_name].value)
            systems[system_name] = new_status

            snackbar_message = (
                f"⚠️ Система {'Включена' if new_status.value else 'Выключена'}."
            )
            update_setting_status(
                status=new_status, bpid=event.peer.bpid, name=system_name
            )

        else:
            snackbar_message = f"⚙️ Меню систем модерации ({page}/2)."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Возраст аккаунта: {'Вкл.' if systems['account_age'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "account_age",
                            "page": "1",
                        },
                    ),
                    color_by_status[systems["account_age"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Запрещенные слова: {'Вкл.' if systems['curse_words'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "curse_words",
                            "page": "1",
                        },
                    ),
                    color_by_status[systems["curse_words"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Открытое ЛС: {'Вкл.' if systems['open_pm'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "open_pm",
                            "page": "1",
                        },
                    ),
                    color_by_status[systems["open_pm"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Медленный режим: {'Вкл.' if systems['slow_mode'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "slow_mode",
                            "page": "1",
                        },
                    ),
                    color_by_status[systems["slow_mode"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "systems_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        if page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Фильтрация URL: {'Вкл.' if systems['link_filter'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "link_filter",
                            "page": "2",
                        },
                    ),
                    color_by_status[systems["link_filter"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Усиленная фильтрация URL: {'Вкл.' if systems['hard_link_filter'].value else 'Выкл.'}",
                        payload={
                            "action_name": "systems_settings",
                            "action_context": "change_status",
                            "system_name": "hard_link_filter",
                            "page": "2",
                        },
                    ),
                    color_by_status[systems["hard_link_filter"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"action_name": "systems_settings", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Включение\\Выключение систем модерации:"
        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )
        self.snackbar(event, snackbar_message)

        return True


class FiltersSettings(BaseAction):
    NAME = "filters_settings"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload

        filters = get_destinated_settings_status(
            destination=SettingDestination.filter, bpid=event.peer.bpid
        )
        color_by_status = {
            SettingStatus.inactive: ButtonColor.NEGATIVE,
            SettingStatus.active: ButtonColor.POSITIVE,
        }

        page = int(payload.get("page", 1))

        if payload.get("action_context") == "change_status":
            filter_name = payload.get("filter_name")
            new_status = SettingStatus(not filters[filter_name].value)
            filters[filter_name] = new_status

            snackbar_message = (
                f"⚠️ Система {'Включена' if not new_status.value else 'Выключена'}."
            )
            update_setting_status(
                status=new_status, bpid=event.peer.bpid, name=filter_name
            )

        else:
            snackbar_message = f"⚙️ Меню фильтров сообщений ({page}/4)."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Приложения: {'Запр.' if filters['app_action'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "app_action",
                            "page": "1",
                        },
                    ),
                    color_by_status[filters["app_action"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Музыка: {'Запр.' if filters['audio'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "audio",
                            "page": "1",
                        },
                    ),
                    color_by_status[filters["audio"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Аудио: {'Запр.' if filters['audio_message'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "audio_message",
                            "page": "1",
                        },
                    ),
                    color_by_status[filters["audio_message"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Файлы: {'Запр.' if filters['doc'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "doc",
                            "page": "1",
                        },
                    ),
                    color_by_status[filters["doc"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "filters_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Пересыл: {'Запр.' if filters['forward'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "forward",
                            "page": "2",
                        },
                    ),
                    color_by_status[filters["forward"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Ответ: {'Запр.' if filters['reply'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "reply",
                            "page": "2",
                        },
                    ),
                    color_by_status[filters["reply"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Граффити: {'Запр.' if filters['graffiti'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "graffiti",
                            "page": "2",
                        },
                    ),
                    color_by_status[filters["graffiti"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Стикеры: {'Запр.' if filters['sticker'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "sticker",
                            "page": "2",
                        },
                    ),
                    color_by_status[filters["sticker"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"action_name": "filters_settings", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "filters_settings", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 3:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Линки: {'Запр.' if filters['link'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "link",
                            "page": "3",
                        },
                    ),
                    color_by_status[filters["link"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Изображения: {'Запр.' if filters['photo'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "photo",
                            "page": "3",
                        },
                    ),
                    color_by_status[filters["photo"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Опросы: {'Запр.' if filters['poll'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "poll",
                            "page": "3",
                        },
                    ),
                    color_by_status[filters["poll"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Видео: {'Запр.' if filters['video'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "video",
                            "page": "3",
                        },
                    ),
                    color_by_status[filters["video"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"action_name": "filters_settings", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "filters_settings", "page": "4"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 4:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label=f"Записи: {'Запр.' if filters['wall'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "wall",
                            "page": "4",
                        },
                    ),
                    color_by_status[filters["wall"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label=f"Геопозиция: {'Запр.' if filters['geo'].value else 'Раз.'}",
                        payload={
                            "action_name": "filters_settings",
                            "action_context": "change_status",
                            "filter_name": "geo",
                            "page": "4",
                        },
                    ),
                    color_by_status[filters["geo"]],
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"action_name": "filters_settings", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Включение\\Выключение фильтров сообщений:"
        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class ChangeDelay(BaseAction):
    NAME = "change_delay"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        setting_name = payload.get("setting_name")

        delay = get_setting_delay(name=setting_name, bpid=event.peer.bpid)

        action_context = payload.get("action_context")
        if action_context is not None:
            time = int(payload.get("time"))

            if action_context == "subtract_time":
                delay = delay - time
                delay = delay if delay > 0 else 0
                snackbar_message = "⚠️ Время уменьшено."

            elif action_context == "add_time":
                delay = delay + time
                snackbar_message = "⚠️ Время увеличено."

            update_setting_delay(name=setting_name, bpid=event.peer.bpid, delay=delay)

        else:
            snackbar_message = "⚙️ Меню установки задержки."

        descriptions = {
            "slow_mode": (
                "⚙️ Задержка для данного чата установлена на:",
                self._get_min_declension,
            ),
            "account_age": (
                "⚙️ Критерий новизны аккаунта для данного чата установлен на:",
                self._get_day_declension,
            ),
            "menu_session": (
                "⚙️ Время жизни сессии меню установлена на:",
                self._get_min_declension,
            ),
            "red_zone": (
                "⚙️ Время истечения срока наказания для красной зоны установлено на:",
                self._get_day_declension,
            ),
            "yellow_zone": (
                "⚙️ Время истечения срока наказания для жёлтой зоны установлено на:",
                self._get_day_declension,
            ),
            "green_zone": (
                "⚙️ Время истечения срока наказания для зелёной зоны установлено на:",
                self._get_day_declension,
            ),
        }

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="- 1 ед.",
                    payload={
                        "action_name": "change_delay",
                        "action_context": "subtract_time",
                        "setting_name": setting_name,
                        "time": 1,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 1 ед.",
                    payload={
                        "action_name": "change_delay",
                        "action_context": "add_time",
                        "setting_name": setting_name,
                        "time": 1,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(
                    label="- 10 ед.",
                    payload={
                        "action_name": "change_delay",
                        "action_context": "subtract_time",
                        "setting_name": setting_name,
                        "time": 10,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 10 ед.",
                    payload={
                        "action_name": "change_delay",
                        "action_context": "add_time",
                        "setting_name": setting_name,
                        "time": 10,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                ButtonColor.SECONDARY,
            )
        )

        text, declension = descriptions[setting_name]
        new_msg_text = f"{text} {delay} {declension(delay)}"

        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
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
class SystemsPunishment(BaseAction):
    NAME = "systems_punishment"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        page = int(payload.get("page", 1))

        snackbar_message = f"⚙️ Меню систем модерации ({page}/2).."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label="Возраст аккаунта",
                        payload={
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                        payload={"action_name": "systems_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        if page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label="Фильтрация URL",
                        payload={
                            "action_name": "change_punishment",
                            "setting_name": "link_filter",
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
                            "action_name": "change_punishment",
                            "setting_name": "hard_link_filter",
                            "page": "2",
                        },
                    ),
                    ButtonColor.PRIMARY,
                )
                .add_row()
                .add_button(
                    Callback(
                        label="<--",
                        payload={"action_name": "systems_punishment", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Выберете необходимую систему:"
        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


class FiltersPunishment(BaseAction):
    NAME = "filters_punishment"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        page = int(payload.get("page", 1))

        snackbar_message = f"⚙️ Меню фильтров сообщений ({page}/4)."

        if page == 1:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label="Приложения",
                        payload={
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                        payload={"action_name": "filters_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 2:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label="Пересыл",
                        payload={
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                        payload={"action_name": "filters_punishment", "page": "1"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "filters_punishment", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 3:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uudi)
                .add_row()
                .add_button(
                    Callback(
                        label="Линки",
                        payload={
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                        payload={"action_name": "filters_punishment", "page": "2"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_button(
                    Callback(
                        label="-->",
                        payload={"action_name": "filters_punishment", "page": "4"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        elif page == 4:
            keyboard = (
                Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
                .add_row()
                .add_button(
                    Callback(
                        label="Записи",
                        payload={
                            "action_name": "change_punishment",
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
                            "action_name": "change_punishment",
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
                        payload={"action_name": "filters_punishment", "page": "3"},
                    ),
                    ButtonColor.SECONDARY,
                )
                .add_row()
                .add_button(
                    Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                    ButtonColor.SECONDARY,
                )
            )

        new_msg_text = "⚙️ Выберете необходимый фильтр:"
        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
            message=new_msg_text,
            keyboard=keyboard.json,
        )

        self.snackbar(event, snackbar_message)

        return True


class ChangePunishment(BaseAction):
    NAME = "change_punishment"

    def _handle(self, event: BaseEvent) -> bool:
        payload = event.button.payload
        setting_name = payload.get("setting_name")

        points = get_setting_points(bpid=event.peer.bpid, name=setting_name)

        action_context = payload.get("action_context")
        if action_context is not None:
            points_delta = payload.get("points")

            if action_context == "subtract_points":
                points = points - points_delta
                points = points if points > 0 else 0
                snackbar_message = "⚠️ Наказание уменьшено."

            elif action_context == "add_points":
                points = points + points_delta
                points = points if points <= 10 else 10
                snackbar_message = "⚠️ Наказание увеличено."

            update_setting_points(
                bpid=event.peer.bpid, name=setting_name, points=points
            )

        else:
            snackbar_message = "⚙️ Меню установки наказания."

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(
                    label="- 1 пред.",
                    payload={
                        "action_name": "change_punishment",
                        "setting_name": setting_name,
                        "action_context": "subtract_points",
                        "points": 1,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 1 пред.",
                    payload={
                        "action_name": "change_punishment",
                        "setting_name": setting_name,
                        "action_context": "add_points",
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
                        "action_name": "change_punishment",
                        "setting_name": setting_name,
                        "action_context": "subtract_points",
                        "points": 3,
                    },
                ),
                ButtonColor.NEGATIVE,
            )
            .add_button(
                Callback(
                    label="+ 3 пред.",
                    payload={
                        "action_name": "change_punishment",
                        "setting_name": setting_name,
                        "action_context": "add_points",
                        "points": 3,
                    },
                ),
                ButtonColor.POSITIVE,
            )
            .add_row()
            .add_button(
                Callback(label="Закрыть", payload={"action_name": "close_menu"}),
                ButtonColor.SECONDARY,
            )
        )

        new_msg_text = (
            f"⚙️ Наказание для настройки {setting_name} установлено на: "
            f"{points} {self._get_warn_declension(points)}."
        )

        self.api.messages.edit(
            peer_id=event.peer.bpid,
            conversation_message_id=event.button.cmid,
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
