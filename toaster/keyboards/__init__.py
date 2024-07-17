"""VK keyboard builder module."""

from .color import ButtonColor
from .keyboard import Keyboard
from .action import Text, OpenLink, OpenApp, Location, VKPay, Callback
from .answer import SnackbarAnswer, AppAnswer, LinkAnswer

# TODO: Этот модуль работает, и работает хорошо. В будущем, наврное, надо переписать его под декларативный стиль.

__all__ = (
    "ButtonColor",
    "Keyboard",
    "Text",
    "OpenLink",
    "OpenApp",
    "Location",
    "VKPay",
    "Callback",
    "SnackbarAnswer",
    "AppAnswer",
    "LinkAnswer",
)
