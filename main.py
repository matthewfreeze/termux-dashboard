import shutil
import platform
import os
import psutil
import requests
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

def get_battery_info():
    """Try to get battery info from sysfs since termux-api is shaky."""
    try:
        # Common paths on Android
        paths = [
            "/sys/class/power_supply/battery/capacity",
            "/sys/class/power_supply/BAT0/capacity"
        ]
        for path in paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    capacity = f.read().strip()
                return f"{capacity}%"
        return "Unknown"
    except Exception:
        return "N/A"

def get_public_ip():
    """Fetch public IP quickly."""
    try:
        return requests.get("https://api.ipify.org", timeout=2).text
    except Exception:
        return "Offline"

def get_weather():
    """Fetch simple weather line."""
    try:
        # Format 1 gives a one-line summary
        return requests.get("https://wttr.in/?format=1", timeout=3).text.strip()
    except Exception:
        return "Weather unavailable"

def create_header():
    """Create the header panel."""
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(
        Text(f"Termux Dashboard • {datetime.now().strftime('%Y-%m-%d %H:%M')}", style="bold cyan")
    )
    return Panel(grid, style="white on blue", box=box.HEAVY)

def create_system_stats():
    """Create system stats table."""
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage("/storage/emulated/0")  # Check internal storage first
    
    table = Table(box=None, expand=True, show_header=False)
    table.add_column("Resource", style="cyan", no_wrap=True)
    table.add_column("Usage", justify="right", style="green", no_wrap=False)  # Allow wrapping

    table.add_row("Memory", f"{mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")
    table.add_row("Storage", f"{disk.used // (1024**3)}GB used / {disk.total // (1024**3)}GB total")
    table.add_row("Public IP", get_public_ip())
    
    return Panel(
        table,
        title="[b]System Status[/b]",
        border_style="green",
        box=box.ROUNDED,
    )

def create_environment_info():
    """Create environment info table."""
    table = Table(box=None, expand=True, show_header=False)
    table.add_column("Component", style="yellow", no_wrap=True)
    table.add_column("Details", justify="right", style="white", no_wrap=False)  # Allow wrapping

    table.add_row("OS", f"Android {platform.release()}")
    table.add_row("Shell", os.environ.get("SHELL", "Unknown"))
    table.add_row("Python", platform.python_version())
    table.add_row("Home", os.environ.get("HOME", "?"))
    
    return Panel(
        table,
        title="[b]Environment[/b]",
        border_style="yellow",
        box=box.ROUNDED,
    )

def main():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Check terminal width to decide layout
    term_width = console.size.width
    if term_width < 100:
        # Stack vertically on narrow screens (phones)
        layout["body"].split_column(
            Layout(name="top_panel"),
            Layout(name="bottom_panel"),
        )
    else:
        # Side by side on wide screens
        layout["body"].split_row(
            Layout(name="top_panel"),
            Layout(name="bottom_panel"),
        )

    layout["header"].update(create_header())
    layout["top_panel"].update(create_system_stats())
    layout["bottom_panel"].update(create_environment_info())
    
    weather = get_weather()
    layout["footer"].update(
        Panel(Align.center(Text(weather, style="bold white")), style="black on grey30", box=box.HEAVY)
    )

    console.print(layout)

if __name__ == "__main__":
    main()
