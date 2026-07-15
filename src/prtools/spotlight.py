from __future__ import annotations

import sys
from typing import Protocol

from prtools.overlays import SpotlightOverlay
from prtools.settings import SpotlightSettings


class SpotlightBackend(Protocol):
    @property
    def diameter(self) -> int: ...

    def set_enabled(self, enabled: bool) -> None: ...

    def set_appearance(self, color: str, opacity: int, diameter: int) -> None: ...

    def sync_position(self) -> None: ...


def create_spotlight(settings: SpotlightSettings) -> SpotlightBackend:
    if sys.platform == "win32":
        from prtools.windows_cursor import WindowsCursorSpotlight

        return WindowsCursorSpotlight(settings)
    return SpotlightOverlay(settings)
