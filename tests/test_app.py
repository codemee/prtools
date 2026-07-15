from PySide6.QtCore import QObject, Signal

from prtools.app import AppController
from prtools.settings import AppSettings


class MemoryStore:
    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or AppSettings.defaults()
        self.save_count = 0

    def load(self) -> AppSettings:
        return self.settings

    def save(self, settings: AppSettings) -> None:
        self.settings = settings
        self.save_count += 1


class FakeMonitor(QObject):
    chord_pressed = Signal(str)
    all_released = Signal()
    failed = Signal(str)

    def __init__(self, succeeds: bool = True) -> None:
        super().__init__()
        self.succeeds = succeeds
        self.running = False
        self.stop_count = 0

    def start(self) -> tuple[bool, str | None]:
        self.running = self.succeeds
        return (True, None) if self.succeeds else (False, "permission denied")

    def stop(self) -> None:
        self.running = False
        self.stop_count += 1


def test_controller_applies_live_spotlight_settings(qapp) -> None:
    store = MemoryStore()
    monitor = FakeMonitor()
    controller = AppController(qapp, store, monitor)  # type: ignore[arg-type]

    controller.set_spotlight_size(208)
    controller.set_spotlight_opacity(61)

    assert controller.spotlight.diameter == 208
    assert store.settings.spotlight.size == 208
    assert store.settings.spotlight.opacity == 61


def test_keyboard_failure_reverts_enabled_state(qapp, monkeypatch) -> None:
    store = MemoryStore()
    monitor = FakeMonitor(succeeds=False)
    controller = AppController(qapp, store, monitor)  # type: ignore[arg-type]
    warnings: list[str] = []
    monkeypatch.setattr(controller.tray, "notify_warning", warnings.append)

    controller.set_keystroke_enabled(True)

    assert not store.settings.keystroke.enabled
    assert not controller.tray.panel.keystroke_enabled.isChecked()
    assert warnings and "permission denied" in warnings[0]


def test_cleanup_stops_effects(qapp) -> None:
    store = MemoryStore()
    monitor = FakeMonitor()
    controller = AppController(qapp, store, monitor)  # type: ignore[arg-type]
    controller.set_spotlight_enabled(True)
    controller.set_keystroke_enabled(True)

    controller.cleanup()

    assert not controller.spotlight.isVisible()
    assert not monitor.running
    assert monitor.stop_count == 1
