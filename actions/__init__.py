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
}


__all__ = ("action_list",)
