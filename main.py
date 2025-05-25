# main.py
import json
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Static
from color_store import load_colors
from textual import events
from color_store import load_colors, load_favorites, save_favorites

# 🎨 Load pywal colors
with open(Path.home() / ".cache/wal/colors.json") as f:
    wal_colors = json.load(f)
    background = wal_colors["special"]["background"].lstrip("#")
    accent = wal_colors["colors"]["color9"].lstrip("#")

class ColorItem(ListItem):
    def __init__(self, color: str, timestamp: int, is_fav: bool = False):
        fav_emoji = "★" if is_fav else "☆"
        swatch = f"[#{color}]█[/] "
        self.label = Static(f"{fav_emoji}{swatch} [b]{color}[/]  •  [dim]{timestamp}[/dim]", markup=True)
        super().__init__(self.label, id=f"c_{color}")
        self.color = color
        self.timestamp = timestamp
        self.is_fav = is_fav

class PaletteVault(App):
    async def on_mount(self) -> None:
        colors = load_colors()
        self.list_view = ListView()  # Only create one list view
        await self.mount(self.list_view)

        favorites = load_favorites()
        for entry in colors:
            hex_code = entry["hex"].lstrip("#").upper()
            is_fav = hex_code in favorites
            await self.list_view.append(ColorItem(hex_code, entry["timestamp"], is_fav))

    async def on_key(self, event: events.Key) -> None:
        if event.key == "f":
            selected = self.list_view.index
            if selected is not None and selected < len(self.list_view.children):
                item = self.list_view.children[selected]
                if isinstance(item, ColorItem):
                    favs = load_favorites()
                    hex_code = item.color.upper()
                    if hex_code in favs:
                        favs.remove(hex_code)
                        item.is_fav = False
                    else:
                        favs.add(hex_code)
                        item.is_fav = True
                    save_favorites(favs)

                    # Update label with new star
                    star = "★" if item.is_fav else "☆"
                    swatch = f"[#{item.color}]█[/] "
                    item.label.update(f"{star}{swatch} [b]{item.color}[/] ({item.timestamp})")

if __name__ == "__main__":
    app = PaletteVault()
    app.run()
