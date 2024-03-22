from .actions import (
    NotMessageOwnerAction,
    CancelAction
)


action_list = {
    # not msg owner -----------------------------
    "not_msg_owner": NotMessageOwnerAction,
    # cancel command ----------------------------
    "cancel_command": CancelAction,
}


__all__ = (
    "action_list",
)
