import json
from pathlib import Path
from datetime import datetime

# Define storage paths
STORAGE_PATH = Path.home() / ".local/share/hyprpicker"
STORAGE_FILE = STORAGE_PATH / "colors.json"
FAV_FILE = Path("favorites.json")  # You can move this to ~/.config if you want later

def ensure_storage():
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    if not STORAGE_FILE.exists():
        with open(STORAGE_FILE, "w") as f:
            json.dump([], f)

def load_colors():
    ensure_storage()
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_color(hex_color: str):
    ensure_storage()
    hex_color = hex_color.strip().lstrip("#").upper()
    if not hex_color:
        return

    colors = load_colors()

    # Avoid duplicates
    if any(entry["hex"].upper() == hex_color for entry in colors):
        return

    colors.append({
        "hex": hex_color,
        "timestamp": int(datetime.now().timestamp())
    })

    with open(STORAGE_FILE, "w") as f:
        json.dump(colors, f, indent=2)

def load_favorites():
    if FAV_FILE.exists():
        with open(FAV_FILE) as f:
            return set(json.load(f))
    return set()

def save_favorites(favs):
    with open(FAV_FILE, "w") as f:
        json.dump(list(favs), f)

def clear_colors():
    with open(STORAGE_FILE, "w") as f:
        json.dump([], f)
