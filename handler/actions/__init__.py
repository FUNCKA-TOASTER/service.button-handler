from .actions import (
    NotMessageOwnerAction,
    CancelAction,
    TestAction,
    MarkAsChatAction,
    MarkAsLogAction,
    UpdateConvDataAction,
    DropMarkAction,
    SetAdministratorPermissionAction,
    SetModeratorPermissionAction,
    SetUserPermissionAction
)


action_list = {
    # not msg owner -----------------------------
    "not_msg_owner": NotMessageOwnerAction,
    # cancel command ----------------------------
    "cancel_command": CancelAction,
    # test --------------------------------------
    "negative_test": TestAction,
    "positive_test": TestAction,
    # mark --------------------------------------
    "mark_as_chat": MarkAsChatAction,
    "mark_as_log": MarkAsLogAction,
    "update_conv_data": UpdateConvDataAction,
    "drop_mark": DropMarkAction,
    # permission --------------------------------
    "set_administrator_permission": SetAdministratorPermissionAction,
    "set_moderator_permission": SetModeratorPermissionAction,
    "set_user_permission": SetUserPermissionAction
}


__all__ = (
    "action_list",
)
