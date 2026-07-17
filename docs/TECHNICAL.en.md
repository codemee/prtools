# Technical Design

[繁體中文](TECHNICAL.md) | [English](TECHNICAL.en.md)

This document describes Presenter Toolkit's cross-platform backends, native macOS integration, and related security boundaries.

## Components and data flow

`AppController` reads and writes settings and coordinates the system tray, spotlight, keyboard monitor, and keystroke overlay. The keyboard backend starts only after the tray panel closes so that event monitoring is not initialized inside the native macOS menu-tracking loop. The backend emits unformatted key-down and key-up events only. `KeyChordTracker` removes duplicate events and maintains the current key set, while `KeystrokeOverlay` displays the last complete combination and delays its fade-out until every key is released.

## macOS spotlight and overlays

macOS has no public API that lets a background application replace the system cursor across applications. The spotlight therefore uses a transparent Qt tool window that follows `QCursor`. The native Cocoa window applies these additional constraints:

- `NSFloatingWindowLevel`: above normal application windows but below the menu bar and pop-up menus.
- `NSWindowStyleMaskNonactivatingPanel` and `WA_ShowWithoutActivating`: showing the overlay does not make it the key window.
- `hidesOnDeactivate = false`: the overlay remains visible when another application becomes active.
- Shadows, borders, and opaque backgrounds are disabled, and all mouse events are ignored.
- The window joins every Space and can appear in full-screen auxiliary spaces.

The cursor position is synchronized once before the tray panel opens. This prevents the spotlight from remaining at a stale position when the native menu-tracking loop pauses Qt timers.

## macOS keyboard monitoring

On macOS, the application creates a Core Graphics event tap using `CGEventTapCreate` at `kCGHIDEventTap` / `kCGHeadInsertEventTap`, always with `kCGEventTapOptionListenOnly`. The HID frontend receives a copy before Carbon global shortcuts or other shortcut utilities handle the event. Listen-only mode guarantees that the callback's return value cannot stop the event from continuing to its destination.

The event tap runs on a dedicated Core Foundation run loop. Its callback never manipulates Qt widgets or timers; it emits a Qt signal to queue data on the main thread. Monitoring is limited to `keyDown`, `keyUp`, and `flagsChanged`:

- Modifier state is rebuilt from event flags to prevent missing or duplicate events from producing stuck keys.
- Left and right modifiers are merged into the displayed Command, Shift, Option, and Control states.
- Keycode 255 is a system-state event and is ignored.
- Caps Lock is displayed as a one-shot key and does not remain in a combination while the lock is active.
- ANSI letters, numbers, arrow keys, and common punctuation use physical keycode mappings; typed text is never recorded.

This backend requires the macOS Input Monitoring permission. The application maintains only the current key state in memory and never stores, logs, or transmits keystroke content.

## Other platforms

- On Windows, the spotlight replaces the real system cursor, and an independent watchdog restores it after an unexpected termination. Keyboard monitoring uses `pynput`.
- On Linux, the spotlight uses a transparent overlay and keyboard monitoring uses `pynput`. X11 has the most complete support; Wayland is constrained by global-input and click-through protocols.

## Verification

Run these checks before committing:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

Manual macOS verification should cover moving the cursor into the menu bar, opening the tray panel, changing focus, Chinese and English input methods, ordinary letters and punctuation, modifier combinations, and combinations already registered by another shortcut utility.
