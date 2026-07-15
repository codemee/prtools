from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


def is_wayland() -> bool:
    return (
        bool(os.environ.get("WAYLAND_DISPLAY"))
        or os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
    )


def make_window_click_through(widget: QWidget) -> None:
    """Apply native input transparency in addition to Qt's window flags.

    Every implementation is deliberately best-effort: Qt's own transparent-input
    hint remains active if the native API is unavailable.
    """
    window_id = int(widget.winId())
    try:
        if sys.platform == "win32":
            _make_windows_click_through(window_id)
        elif sys.platform == "darwin":
            _make_macos_click_through(window_id)
        elif sys.platform.startswith("linux") and not is_wayland():
            _make_x11_click_through(window_id)
    except (ImportError, OSError, RuntimeError, AttributeError, TypeError):
        return


def _make_windows_click_through(window_id: int) -> None:
    import ctypes

    user32 = ctypes.windll.user32
    get_window_long = user32.GetWindowLongPtrW
    set_window_long = user32.SetWindowLongPtrW
    index_extended_style = -20
    transparent = 0x00000020
    layered = 0x00080000
    no_activate = 0x08000000
    tool_window = 0x00000080
    current = get_window_long(window_id, index_extended_style)
    set_window_long(
        window_id,
        index_extended_style,
        current | transparent | layered | no_activate | tool_window,
    )


def _make_macos_click_through(window_id: int) -> None:
    import objc

    native_view = objc.objc_object(c_void_p=window_id)
    native_window = native_view.window()
    native_window.setIgnoresMouseEvents_(True)
    native_window.setAcceptsMouseMovedEvents_(False)


def _make_x11_click_through(window_id: int) -> None:
    from Xlib import display
    from Xlib.ext import shape

    connection = display.Display()
    try:
        window = connection.create_resource_object("window", window_id)
        window.shape_rectangles(shape.SO.Set, shape.SK.Input, 0, 0, 0, [])
        connection.sync()
    finally:
        connection.close()
