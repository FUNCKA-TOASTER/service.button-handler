"""Module "actions".

File:
    __init__.py

About:
    Initializing the "actions" module.
"""

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
    ChangeDelay,
    SystemsPunishment,
    FiltersPunishment,
    ChangePunishment,
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
    # Delay\Expire ------------------------------
    ChangeDelay.NAME: ChangeDelay,
    # Punishment --------------------------------
    SystemsPunishment.NAME: SystemsPunishment,
    FiltersPunishment.NAME: FiltersPunishment,
    ChangePunishment.NAME: ChangePunishment,
}


__all__ = ("action_list",)
