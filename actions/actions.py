import random
from toaster.broker.events import Event
from toaster.keyboards import Keyboard, ButtonColor, Callback
from data import TOASTER_DB
from data import UserPermission
from data.scripts import (
    get_peer_mark,
    set_peer_mark,
    drop_peer_mark,
    update_peer_data,
    get_user_permission,
    set_user_permission,
    drop_user_permission,
)
from .base import BaseAction


# ------------------------------------------------------------------------
class Error(BaseAction):
    NAME = "error"

    def _handle(self, event: Event) -> bool:
        snackbar_message = "⚠️ Что-то пошло не так."
        self.snackbar(event, snackbar_message)

        return False


class RejectAccess(BaseAction):
    NAME = "reject_access"

    def _handle(self, event: Event) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."
        self.snackbar(event, snackbar_message)

        return False


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
        mark = get_peer_mark(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
        )

        if mark is None:
            payload = event.button.payload
            mark = payload.get("mark")

            set_peer_mark(
                db_instance=TOASTER_DB,
                mark=mark,
                bpid=event.peer.bpid,
                bpn=event.peer.name,
            )
            snackbar_message = f'📝 Беседа помечена как "{mark}".'

        else:
            snackbar_message = f'❗Беседа уже имеет метку "{mark}".'

        self.snackbar(event, snackbar_message)

        return True


class UpdatePeerData(BaseAction):
    NAME = "update_peer_data"

    def _handle(self, event: Event) -> bool:
        mark = get_peer_mark(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
        )

        if mark is not None:
            update_peer_data(
                db_instance=TOASTER_DB,
                bpid=event.peer.bpid,
                name=event.peer.name,
            )
            snackbar_message = "📝 Данные беседы обновлены."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


class DropMark(BaseAction):
    NAME = "drop_mark"

    def _handle(self, event: Event) -> bool:
        mark = get_peer_mark(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
        )

        if mark is not None:
            drop_peer_mark(
                db_instance=TOASTER_DB,
                bpid=event.peer.bpid,
            )
            snackbar_message = f'📝 Метка "{mark}" снята с беседы.'

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True


# ------------------------------------------------------------------------
class SetPermission(BaseAction):
    NAME = "set_permission"

    def _handle(self, event: Event) -> bool:
        payload = event.button.payload
        target_uuid = payload.get("target")

        current_permission = get_user_permission(
            db_instance=TOASTER_DB,
            uuid=target_uuid,
            bpid=event.peer.bpid,
        )

        new_permission = int(payload.get("permission"))
        role = UserPermission(current_permission)

        if current_permission == 0:
            role = UserPermission(new_permission)
            set_user_permission(
                db_instance=TOASTER_DB,
                uuid=target_uuid,
                bpid=event.peer.bpid,
                lvl=new_permission,
            )
            snackbar_message = f'⚒️ Пользователю назначена роль "{role.name}".'
            self.snackbar(event, snackbar_message)
            return True

        else:
            role = UserPermission(current_permission)
            snackbar_message = f'❗Пользователь уже имеет роль "{role.name}".'
            self.snackbar(event, snackbar_message)
            return False


class DropPermission(BaseAction):
    NAME = "drop_permission"

    def _handle(self, event: Event) -> bool:
        payload = event.button.payload
        target_uuid = payload.get("target")

        current_permission = get_user_permission(
            db_instance=TOASTER_DB,
            uuid=target_uuid,
            bpid=event.peer.bpid,
            ignore_staff=True,
        )

        if current_permission > 0:
            drop_user_permission(
                db_instance=TOASTER_DB,
                uuid=target_uuid,
                bpid=event.peer.bpid,
            )
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

    def _handle(self, event: Event) -> bool:
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

        # TODO: Создать сессию меню

        return True


class GameCoinflip(BaseAction):
    NAME = "game_coinflip"
    EMOJI = ["Орёл 🪙", "Решка 🪙"]

    def _handle(self, event: Event) -> bool:
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

        # TODO: Создать сессию меню

        return True


# ------------------------------------------------------------------------
