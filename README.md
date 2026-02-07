# Termux Dashboard

A simple, beautiful dashboard for Termux on Android.

## Features
- **System Stats:** Memory, Storage, and Battery (if accessible).
- **Environment Info:** OS version, Shell, Python version.
- **Network:** Public IP address.
- **Weather:** Current weather via wttr.in.
- **TUI:** Built with `rich` for a nice terminal interface.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/matthewfreeze/termux-dashboard.git
    cd termux-dashboard
    ```

2.  Install `uv` (if not already installed):
    ```bash
    pip install uv
    ```

3.  Run the dashboard:
    ```bash
    uv run main.py
    ```

## Requirements
- Python 3.12+
- Termux on Android

## License
MIT
