# Presenter Toolkit

[繁體中文](README.md) | [English](README.en.md)

A cross-platform system-tray presentation assistant. The application has no main window; all settings are available from the tray icon's context menu.

## Features

- Spotlight cursor: customizable color, opacity, and circle diameter from 48 to 320 px. Windows uses a real system cursor, while macOS and Linux use a click-through transparent overlay.
- Keystroke display: shows individual keys and key combinations near the bottom center of the screen containing the pointer without intercepting keyboard input.
- Persistent preferences: remembers whether each feature is enabled and restores its appearance settings.
- Multi-monitor and high-DPI support: positions and renders using Qt logical pixels.

## Install with uv tool

Install [uv](https://docs.astral.sh/uv/) first. From a downloaded project directory, run:

```powershell
uv tool install .
prtools
```

You can also install the latest stable release directly from GitHub. The `latest` tag is updated for every stable release:

```powershell
uv tool install git+https://github.com/codemee/prtools.git@latest
prtools
```

To pin a specific release, replace `latest` with a version tag such as `v0.0.1`.

If the `prtools` command is not found after installation, run `uv tool update-shell` and open a new terminal. To remove the tool, run `uv tool uninstall prtools`.

## Run without installing using uvx

From a downloaded project directory, run:

```powershell
uvx --from . prtools
```

Or run the latest stable release directly from GitHub:

```powershell
uvx --from git+https://github.com/codemee/prtools.git@latest prtools
```

`uvx` prepares and runs the application in an isolated environment without persistently installing the `prtools` command in the tool directory.

## Development

uv manages Python 3.12, the virtual environment, and all dependencies:

```powershell
uv sync
uv run prtools
```

Quality checks:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

## Platform notes

- Windows: no additional permissions are required. Enabling the spotlight temporarily replaces the system cursors; they are restored when the feature is disabled or the application exits. The independently running watchdog installed with the tool restores the cursors if the main process terminates unexpectedly.
- macOS: the keystroke display uses a read-only HID-level event monitor. In **System Settings → Privacy & Security → Input Monitoring**, allow the application that launches `prtools`, such as ChatGPT, Terminal, or another terminal application. The monitor never modifies or intercepts events and can observe a key combination before another shortcut utility handles it.
- Linux: full support targets X11. The desktop environment must provide a StatusNotifierItem or XEmbed system tray. GNOME may require an AppIndicator-style extension.
- Wayland: global input and overlay protocol restrictions mean that keystroke monitoring and click-through behavior are not guaranteed. The application displays a warning in its menu.

Keystroke content is used only for the live on-screen display. It is never written to settings, files, or logs.

See the [technical design](docs/TECHNICAL.en.md) for the implementation architecture, native macOS window levels, permission model, and keyboard event flow.
