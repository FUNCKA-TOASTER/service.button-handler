from .actions import (
    Error,
    RejectAccess,
    CloseMenu,
    SetMark,
    UpdatePeerData,
    DropMark,
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
}


__all__ = ("action_list",)
