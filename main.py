# main.py
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import pyperclip
import logging

from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Static, Input
from textual.containers import Container, Vertical, Horizontal
from textual import events, on
from textual.message import Message

from color_store import load_colors, load_favorites, save_favorites
from color_utils import search_colors, get_color_name


def setup_logging(config):
    """Set up logging based on config."""
    debug_config = config.get("debug", {"enabled": False, "level": "INFO"})
    
    if debug_config.get("enabled", False):
        level = getattr(logging, debug_config.get("level", "INFO").upper(), logging.INFO)
        logging.basicConfig(level=level)
    else:
        logging.basicConfig(level=logging.WARNING)
    
    return logging.getLogger(__name__)


def load_config():
    """Load config from various locations in order of precedence."""
    config_locations = [
        Path.home() / ".config" / "pyreto" / "config.json",  # User config
        Path("/etc/pyreto/config.json"),                     # System config
        Path("config.json")                                  # Local config
    ]
    
    for config_path in config_locations:
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
    
    # Default config if none found
    return {
        "colors": {
            "background": "#1e1e2e",
            "accent": "#ff79c6",
            "hover": "#313244",
            "focus": "#45475a",
            "text": "white"
        },
        "pywal": {
            "enabled": True,
            "background_key": "special.background",
            "accent_key": "colors.color9"
        },
        "display": {
            "header_height": "3",
            "item_height": "3",
            "padding": "1"
        },
        "debug": {
            "enabled": False,
            "level": "INFO"
        }
    }


def get_css_path():
    """Get the CSS file path from various locations in order of precedence."""
    css_locations = [
        Path.home() / ".config" / "pyreto" / "app.css",  # User CSS
        Path("/etc/pyreto/app.css"),                     # System CSS
        Path("app.css")                                  # Local CSS
    ]
    
    for css_path in css_locations:
        if css_path.exists():
            return str(css_path)
    
    return "app.css"  # Default to local app.css


def get_colors():
    config = load_config()
    logger = setup_logging(config)
    logger.debug(f"Pywal enabled: {config['pywal']['enabled']}")
    
    # Try loading pywal colors if enabled
    if config["pywal"]["enabled"]:
        try:
            wal_path = Path.home() / ".cache/wal/colors.json"
            logger.debug(f"Looking for Pywal colors at: {wal_path}")
            with open(wal_path) as f:
                wal_colors = json.load(f)
                logger.debug(f"Loaded Pywal colors: {wal_colors}")
                # Get all colors from Pywal
                colors = {
                    "background": wal_colors["special"]["background"].lstrip("#"),
                    "accent": wal_colors["colors"]["color9"].lstrip("#"),
                    "hover": wal_colors["colors"]["color8"].lstrip("#"),
                    "focus": wal_colors["colors"]["color10"].lstrip("#"),
                    "text": wal_colors["special"]["foreground"].lstrip("#"),
                    "header": wal_colors["colors"]["color1"].lstrip("#")
                }
                logger.debug(f"Processed Pywal colors: {colors}")
                return colors
        except Exception as e:
            logger.error(f"Failed to load Pywal colors: {e}")
            pass
    
    # Fallback to config colors
    logger.debug("Falling back to config colors")
    return {
        "background": config["colors"]["background"].lstrip("#"),
        "accent": config["colors"]["accent"].lstrip("#"),
        "hover": config["colors"]["hover"].lstrip("#"),
        "focus": config["colors"]["focus"].lstrip("#"),
        "text": config["colors"]["text"].lstrip("#"),
        "header": config["colors"]["accent"].lstrip("#")  # Use accent color for header as fallback
    }


def human_time(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    delta = now - dt
    if delta < timedelta(minutes=1):
        return "just now"
    if delta < timedelta(hours=1):
        minutes = delta.seconds // 60
        return f"{minutes} min ago"
    if delta < timedelta(days=1):
        hours = delta.seconds // 3600
        return f"{hours} hour(s) ago"
    return dt.strftime("%b %d, %Y")


class ColorItem(ListItem):
    def __init__(self, color: str, timestamp: int, is_fav: bool = False):
        super().__init__(id=f"c_{color}")
        self.color = color
        self.timestamp = timestamp
        self.is_fav = is_fav

    def compose(self) -> ComposeResult:
        yield Static(self.build_label(), id="label", markup=True)

    def toggle_favorite(self):
        self.is_fav = not self.is_fav

    def build_label(self) -> str:
        fav_emoji = "★" if self.is_fav else "☆"
        swatch = f"[#{self.color}]██[/]"  # Bigger swatch
        time_str = human_time(self.timestamp)
        return f"{fav_emoji} {swatch}  [b]{self.color}[/]  •  [dim]{time_str}[/dim]"

    def refresh_label(self):
        label = self.query_one("#label", Static)
        label.update(self.build_label())


class PaletteVault(App):
    show_only_favs = False
    search_query = ""
    sort_reversed = False

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.logger = setup_logging(self.config)
        self.logger.debug(f"Loaded config: {self.config}")
        self.theme_colors = get_colors()
        self.logger.debug(f"Got colors: {self.theme_colors}")
        # Update CSS with current theme
        css_path = get_css_path()
        update_css_with_theme(css_path, self.theme_colors, self.config)
        # Set CSS path directly
        self.CSS = open(css_path).read()
        self.logger.debug("CSS loaded into app")

    def compose(self) -> ComposeResult:
        self.header = Static(id="header")
        self.list_view = ListView()
        yield self.header
        with Horizontal(id="search_container"):
            yield Static("Find:", id="search_label")
            yield Input(placeholder="Search colors...", id="search_input")
        yield self.list_view

    async def on_mount(self) -> None:
        await self.rebuild_list()
        self.update_header()

    def update_header(self):
        view_type = "Favorites" if self.show_only_favs else "Color Palette Database"
        sort_indicator = "↓" if self.sort_reversed else "↑"
        self.header.update(f"Pyreto - {view_type} {sort_indicator}")

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id == "search_input":
            self.search_query = event.value
            await self.rebuild_list()

    async def on_key(self, event: events.Key) -> None:
        self.logger.debug(f"Key pressed: {event.key}")
        
        selected = self.list_view.index

        if event.key == "f":
            if not self.is_valid_selection(selected):
                self.notify("No color selected! Please select a color first.")
                return
                
            item = self.list_view.children[selected]
            if isinstance(item, ColorItem):
                favs = load_favorites()
                hex_code = item.color.upper()
                if item.is_fav:
                    favs.discard(hex_code)
                    self.notify(f"Removed #{hex_code} from favorites")
                else:
                    favs.add(hex_code)
                    self.notify(f"Added #{hex_code} to favorites")
                item.toggle_favorite()
                item.refresh_label()
                save_favorites(favs)
                await self.rebuild_list()

        elif event.key == "h":
            self.show_only_favs = not self.show_only_favs
            self.update_header()
            await self.rebuild_list()

        elif event.key == "s":
            self.sort_reversed = not self.sort_reversed
            self.update_header()
            await self.rebuild_list()

        elif event.key == "c":
            if not self.is_valid_selection(selected):
                self.notify("No color selected! Please select a color first.")
                return
                
            item = self.list_view.children[selected]
            if isinstance(item, ColorItem):
                pyperclip.copy(f"#{item.color}")
                self.notify(f"Copied #{item.color} to clipboard!")

    def is_valid_selection(self, index: int) -> bool:
        """Check if the given index is a valid selection in the list view."""
        return 0 <= index < len(self.list_view.children)

    async def rebuild_list(self):
        favs = load_favorites()
        colors = load_colors()

        # Sort so favorites come first
        colors.sort(key=lambda x: x["hex"].lstrip("#").upper() not in favs)

        # Sort by timestamp
        colors.sort(key=lambda x: x["timestamp"], reverse=self.sort_reversed)

        # Clear the list view first
        await self.list_view.clear()

        # Filter colors based on search query
        if self.search_query:
            filtered_colors = search_colors(self.search_query, [c["hex"].lstrip("#").upper() for c in colors])
            colors = [c for c in colors if c["hex"].lstrip("#").upper() in filtered_colors]

        for entry in colors:
            hex_code = entry.get("hex", "").lstrip("#").upper()
            timestamp = entry.get("timestamp", 0)
            is_fav = hex_code in favs

            if self.show_only_favs and not is_fav:
                continue

            await self.list_view.append(ColorItem(hex_code, timestamp, is_fav))


def verify_css_content(css_path: str) -> None:
    """Verify the CSS content after updating."""
    try:
        with open(css_path, 'r') as f:
            content = f.read()
            # Only log if debug is enabled
            config = load_config()
            if config.get("debug", {}).get("enabled", False):
                logger = setup_logging(config)
            logger.debug(f"Current CSS content:\n{content}")
    except Exception as e:
        config = load_config()
        logger = setup_logging(config)
        logger.error(f"Failed to verify CSS content: {e}")


def update_css_with_theme(css_path: str, colors: dict, config: dict) -> None:
    """Update the CSS file with the current theme colors."""
    logger = setup_logging(config)
    logger.debug(f"Updating CSS with theme colors: {colors}")
    with open(css_path, 'r') as f:
        css_content = f.read()
    
    # Create a mapping of all color replacements
    color_map = {
        '#1e1e2e': f'#{colors["background"]}',
        '#ff79c6': f'#{colors["accent"]}',
        '#313244': f'#{colors["hover"]}',
        '#45475a': f'#{colors["focus"]}',
        'white':   f'#{colors["text"]}',
        '#040D16': f'#{colors["background"]}',  # Additional background color
        '#CC9A60': f'#{colors["accent"]}',      # Additional accent color
        '#1a1b26': f'#{colors["background"]}',  # Additional background color
        '#7aa2f7': f'#{colors["accent"]}',      # Additional accent color
        '#24283b': f'#{colors["hover"]}',       # Additional hover color
        '#414868': f'#{colors["focus"]}',       # Additional focus color
        '#ff0000': f'#{colors["header"]}',      # Header color
        '#F6D175': f'#{colors["focus"]}',       # Focus/highlight color for ListView
        '#859796': f'#{colors["hover"]}',       # Hover color
        '#bfd9d7': f'#{colors["text"]}',        # Text color
    }
    
    logger.debug(f"Color mapping: {color_map}")
    
    # Apply all color replacements
    for old_color, new_color in color_map.items():
        css_content = css_content.replace(old_color, new_color)
    
    # Write updated CSS
    with open(css_path, 'w') as f:
        f.write(css_content)
    logger.debug(f"CSS file updated at {css_path}")
    
    # Verify the CSS content
    verify_css_content(css_path)


if __name__ == "__main__":
    app = PaletteVault()
    app.run()
