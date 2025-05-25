from typing import Dict, List, Tuple
import colorsys
import math

# Basic color name database (we can expand this later)
COLOR_NAMES: Dict[str, str] = {
    "FF0000": "red",
    "00FF00": "green",
    "0000FF": "blue",
    "FFFF00": "yellow",
    "FF00FF": "magenta",
    "00FFFF": "cyan",
    "000000": "black",
    "FFFFFF": "white",
    "808080": "gray",
    "800000": "maroon",
    "808000": "olive",
    "008000": "dark green",
    "800080": "purple",
    "008080": "teal",
    "000080": "navy",
    "FFA500": "orange",
    "A52A2A": "brown",
    "FFC0CB": "pink",
    "FFD700": "gold",
    "E6E6FA": "lavender",
}

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def color_distance(color1: str, color2: str) -> float:
    """Calculate color distance using a weighted RGB distance."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Convert to float and normalize
    r1, g1, b1 = [x/255.0 for x in rgb1]
    r2, g2, b2 = [x/255.0 for x in rgb2]
    
    # Calculate weighted distance
    return math.sqrt(
        2 * (r1 - r2) ** 2 +
        4 * (g1 - g2) ** 2 +
        3 * (b1 - b2) ** 2
    )

def get_color_name(hex_color: str) -> str:
    """Get the name of a color from the database."""
    hex_color = hex_color.lstrip("#").upper()
    return COLOR_NAMES.get(hex_color, "")

def find_similar_colors(target_color: str, colors: List[str], max_distance: float = 0.5) -> List[str]:
    """Find colors similar to the target color."""
    similar = []
    for color in colors:
        distance = color_distance(target_color, color)
        if distance <= max_distance:
            similar.append((color, distance))
    
    # Sort by distance
    similar.sort(key=lambda x: x[1])
    return [color for color, _ in similar]

def search_colors(query: str, colors: List[str]) -> List[str]:
    """Search colors using multiple matching strategies."""
    query = query.lower().strip()
    if not query:
        return colors
    
    results = set()
    
    # 1. Direct hex match
    for color in colors:
        if query in color.lower():
            results.add(color)
    
    # 2. Color name match
    for hex_color, name in COLOR_NAMES.items():
        if query in name.lower():
            results.add(hex_color)
    
    # 3. Try to interpret query as a color
    if len(query) >= 3:  # Minimum length for a color
        try:
            # Try to find similar colors
            similar = find_similar_colors(f"#{query}", colors)
            results.update(similar)
        except ValueError:
            pass
    
    return list(results) 