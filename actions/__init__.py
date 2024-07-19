from .actions import (
    Error,
    RejectAccess,
    CloseMenu,
    SetMark,
    UpdatePeerData,
    DropMark,
    SetPermission,
    DropPermission,
    GameCoinflip,
    GameRoll,
    SystemsSettings,
    FiltersSettings,
)


action_list = {
    # system ------------------------------------
    Error.NAME: Error,
    RejectAccess.NAME: RejectAccess,
    CloseMenu.NAME: CloseMenu,
    # mark --------------------------------------
    SetMark.NAME: SetMark,
    UpdatePeerData.NAME: UpdatePeerData,
    DropMark.NAME: DropMark,
    # permission --------------------------------
    SetPermission.NAME: SetPermission,
    DropPermission.NAME: DropPermission,
    # Game  -------------------------------------
    GameCoinflip.NAME: GameCoinflip,
    GameRoll.NAME: GameRoll,
    # Settings ----------------------------------
    SystemsSettings.NAME: SystemsSettings,
    FiltersSettings.NAME: FiltersSettings,
}


__all__ = ("action_list",)
