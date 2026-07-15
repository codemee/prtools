from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal

from prtools.keys import KeyChordTracker


class KeyboardMonitor(QObject):
    chord_pressed = Signal(str)
    all_released = Signal()
    failed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._listener: Any | None = None
        self._tracker = KeyChordTracker()

    @property
    def running(self) -> bool:
        return self._listener is not None

    def start(self) -> tuple[bool, str | None]:
        if self._listener is not None:
            return True, None
        try:
            from pynput import keyboard

            listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
            listener.start()
            listener.wait()
            self._listener = listener
        except Exception as error:  # pynput exposes backend-specific exceptions
            self._listener = None
            self._tracker.clear()
            return False, str(error)
        return True, None

    def stop(self) -> None:
        listener, self._listener = self._listener, None
        self._tracker.clear()
        if listener is not None:
            listener.stop()

    def _on_press(self, key: object) -> None:
        try:
            label = self._tracker.press(key)
            if label:
                self.chord_pressed.emit(label)
        except Exception as error:
            self.failed.emit(str(error))

    def _on_release(self, key: object) -> None:
        try:
            if self._tracker.release(key):
                self.all_released.emit()
        except Exception as error:
            self.failed.emit(str(error))
