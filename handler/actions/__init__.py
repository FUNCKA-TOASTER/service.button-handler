from .actions import (
    NotMessageOwnerAction,
    CancelAction,
    MarkAction,
    UpdateConvDataAction,
    DropMarkAction,
    SetPermissionAction,
    GameRollAction,
    GameCoinflipAction,
    SystemSettingsAction,
    FilterSettingsAction,
    SlowModeDelayAction,
    AccountAgeDelayAction
)


action_list = {
    # not msg owner -----------------------------
    NotMessageOwnerAction.NAME: NotMessageOwnerAction,
    # cancel command ----------------------------
    CancelAction.NAME: CancelAction,
    # mark --------------------------------------
    MarkAction.NAME: MarkAction,
    UpdateConvDataAction.NAME: UpdateConvDataAction,
    DropMarkAction.NAME: DropMarkAction,
    # permission --------------------------------
    SetPermissionAction.NAME: SetPermissionAction,
    # game --------------------------------------
    GameRollAction.NAME: GameRollAction,
    GameCoinflipAction.NAME: GameCoinflipAction,
    # settings ----------------------------------
    SystemSettingsAction.NAME: SystemSettingsAction,
    FilterSettingsAction.NAME: FilterSettingsAction,
    # delay -------------------------------------
    SlowModeDelayAction.NAME: SlowModeDelayAction,
    AccountAgeDelayAction.NAME: AccountAgeDelayAction
}


__all__ = (
    "action_list",
)
