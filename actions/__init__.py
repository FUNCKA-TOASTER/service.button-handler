from .actions import (
    RejectAccess,
    CloseMenu,
    SetMark,
)


action_list = {
    # system ------------------------------------
    RejectAccess.NAME: RejectAccess,
    CloseMenu.NAME: CloseMenu,
    # mark --------------------------------------
    SetMark.NAME: SetMark,
}


__all__ = ("action_list",)
