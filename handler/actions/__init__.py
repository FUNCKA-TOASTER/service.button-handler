from .actions import (
    NotMessageOwnerAction,
    CancelAction,
    MarkAction,
    UpdateConvDataAction,
    DropMarkAction,
    SetPermissionAction,
    GameRollAction,
    GameCoinflipAction,
    SystemsSettingsAction,
    FiltersSettingsAction,
    ChangeDelayAction,
    GreenZoneDelayAction,
    YellowZoneDelayAction,
    RedZoneDelayAction,
    SystemsPunishmentAction,
    FiltersPunishmentAction,
    ChangePunishmentAction,
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
    SystemsSettingsAction.NAME: SystemsSettingsAction,
    FiltersSettingsAction.NAME: FiltersSettingsAction,
    # delay -------------------------------------
    ChangeDelayAction.NAME: ChangeDelayAction,
    # expire ------------------------------------
    GreenZoneDelayAction.NAME: GreenZoneDelayAction,
    YellowZoneDelayAction.NAME: YellowZoneDelayAction,
    RedZoneDelayAction.NAME: RedZoneDelayAction,
    # punishment --------------------------------
    SystemsPunishmentAction.NAME: SystemsPunishmentAction,
    FiltersPunishmentAction.NAME: FiltersPunishmentAction,
    ChangePunishmentAction.NAME: ChangePunishmentAction,
}


__all__ = ("action_list",)
