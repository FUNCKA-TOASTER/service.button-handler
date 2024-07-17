from .actions import (
    Error,
    RejectAccess,
    CloseMenu,
    # SetMark,
)


action_list = {
    # system ------------------------------------
    Error.NAME: Error,
    RejectAccess.NAME: RejectAccess,
    CloseMenu.NAME: CloseMenu,
    # mark --------------------------------------
    # SetMark.NAME: SetMark,
}


__all__ = ("action_list",)
