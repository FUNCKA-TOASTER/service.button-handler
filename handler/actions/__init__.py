from .actions import (
    NotMessageOwnerAction,
    CancelAction,
    MarkAsChatAction,
    MarkAsLogAction,
    UpdateConvDataAction,
    DropMarkAction,
    SetAdministratorPermissionAction,
    SetModeratorPermissionAction,
    SetUserPermissionAction,
    GameRollAction,
    GameCoinflipAction,
    SystemSettingsPageOneAction,
    FilterSettingsPageOneAction
)


action_list = {
    # not msg owner -----------------------------
    NotMessageOwnerAction.NAME: NotMessageOwnerAction,
    # cancel command ----------------------------
    CancelAction.NAME: CancelAction,
    # mark --------------------------------------
    MarkAsChatAction.NAME: MarkAsChatAction,
    MarkAsLogAction.NAME: MarkAsLogAction,
    UpdateConvDataAction.NAME: UpdateConvDataAction,
    DropMarkAction.NAME: DropMarkAction,
    # permission --------------------------------
    SetAdministratorPermissionAction.NAME: SetAdministratorPermissionAction,
    SetModeratorPermissionAction.NAME: SetModeratorPermissionAction,
    SetUserPermissionAction.NAME: SetUserPermissionAction,
    # game --------------------------------------
    GameRollAction.NAME: GameRollAction,
    GameCoinflipAction.NAME: GameCoinflipAction,
    # settings ----------------------------------
    SystemSettingsPageOneAction.NAME: SystemSettingsPageOneAction,
    FilterSettingsPageOneAction.NAME: FilterSettingsPageOneAction
}


__all__ = (
    "action_list",
)
