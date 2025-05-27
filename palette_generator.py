import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import colorsys

def hex_to_hsv(hex_color: str) -> tuple:
    """Convert hex color to HSV."""
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    
    # Convert RGB to HSV
    return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_hex(h: float, s: float, v: float) -> str:
    """Convert HSV to hex color."""
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert RGB to hex
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

def generate_analogous_colors(base_color: str, num_colors: int = 5) -> List[str]:
    """Generate analogous colors (colors adjacent on the color wheel)."""
    h, s, v = hex_to_hsv(base_color)
    
    # Generate colors with slight hue variations
    colors = []
    for i in range(num_colors):
        # Rotate hue by 30 degrees (0.083 in HSV)
        new_h = (h + (i - num_colors//2) * 0.083) % 1.0
        colors.append(hsv_to_hex(new_h, s, v))
    
    return colors

def generate_complementary_colors(base_color: str) -> List[str]:
    """Generate complementary colors (opposite on the color wheel)."""
    h, s, v = hex_to_hsv(base_color)
    
    # Generate complementary color by rotating hue by 180 degrees (0.5 in HSV)
    complementary = hsv_to_hex((h + 0.5) % 1.0, s, v)
    
    return [base_color, complementary]

def generate_triadic_colors(base_color: str) -> List[str]:
    """Generate triadic colors (three colors equally spaced on the color wheel)."""
    h, s, v = hex_to_hsv(base_color)
    
    # Generate two additional colors by rotating hue by 120 degrees (0.333 in HSV)
    color2 = hsv_to_hex((h + 0.333) % 1.0, s, v)
    color3 = hsv_to_hex((h + 0.666) % 1.0, s, v)
    
    return [base_color, color2, color3]

def generate_split_complementary_colors(base_color: str) -> List[str]:
    """Generate split complementary colors (base color and two colors adjacent to its complement)."""
    h, s, v = hex_to_hsv(base_color)
    
    # Generate two colors adjacent to the complement
    color2 = hsv_to_hex((h + 0.417) % 1.0, s, v)  # 150 degrees
    color3 = hsv_to_hex((h + 0.583) % 1.0, s, v)  # 210 degrees
    
    return [base_color, color2, color3]

def generate_tetradic_colors(base_color: str) -> List[str]:
    """Generate tetradic colors (four colors arranged into two complementary pairs)."""
    h, s, v = hex_to_hsv(base_color)
    
    # Generate three additional colors
    color2 = hsv_to_hex((h + 0.25) % 1.0, s, v)   # 90 degrees
    color3 = hsv_to_hex((h + 0.5) % 1.0, s, v)    # 180 degrees
    color4 = hsv_to_hex((h + 0.75) % 1.0, s, v)   # 270 degrees
    
    return [base_color, color2, color3, color4]

def save_palette_to_markdown(base_color: str, palette_name: str = None) -> str:
    """Generate and save a color palette to a markdown file."""
    # Generate all palette variations
    analogous = generate_analogous_colors(base_color)
    complementary = generate_complementary_colors(base_color)
    triadic = generate_triadic_colors(base_color)
    split_complementary = generate_split_complementary_colors(base_color)
    tetradic = generate_tetradic_colors(base_color)
    
    # Create markdown content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    palette_name = palette_name or f"Palette from {base_color}"
    
    md_content = f"""# {palette_name}
Generated on {timestamp}

## Base Color
![{base_color}](https://via.placeholder.com/50/{base_color.lstrip('#')}/000000?text=+)

## Analogous Colors
{''.join(f'![{color}](https://via.placeholder.com/50/{color.lstrip("#")}/000000?text=+)' for color in analogous)}

## Complementary Colors
{''.join(f'![{color}](https://via.placeholder.com/50/{color.lstrip("#")}/000000?text=+)' for color in complementary)}

## Triadic Colors
{''.join(f'![{color}](https://via.placeholder.com/50/{color.lstrip("#")}/000000?text=+)' for color in triadic)}

## Split Complementary Colors
{''.join(f'![{color}](https://via.placeholder.com/50/{color.lstrip("#")}/000000?text=+)' for color in split_complementary)}

## Tetradic Colors
{''.join(f'![{color}](https://via.placeholder.com/50/{color.lstrip("#")}/000000?text=+)' for color in tetradic)}

## Color Codes

### Analogous
{chr(10).join(f'- `{color}`' for color in analogous)}

### Complementary
{chr(10).join(f'- `{color}`' for color in complementary)}

### Triadic
{chr(10).join(f'- `{color}`' for color in triadic)}

### Split Complementary
{chr(10).join(f'- `{color}`' for color in split_complementary)}

### Tetradic
{chr(10).join(f'- `{color}`' for color in tetradic)}
"""
    
    # Create Pyreto directory in Documents if it doesn't exist
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    palettes_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the markdown file
    filename = f"palette_{base_color.lstrip('#')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = palettes_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(md_content)
    
    return str(filepath)

def list_saved_palettes() -> List[Dict]:
    """List all saved palettes with their metadata."""
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    if not palettes_dir.exists():
        return []
    
    palettes = []
    for file in palettes_dir.glob("palette_*.md"):
        try:
            with open(file, 'r') as f:
                content = f.read()
                # Extract base color from filename
                base_color = f"#{file.stem.split('_')[1]}"
                # Extract timestamp from filename
                timestamp = datetime.strptime(file.stem.split('_')[2], "%Y%m%d_%H%M%S")
                # Extract palette name from content
                name = content.split('\n')[0].lstrip('# ')
                
                palettes.append({
                    'name': name,
                    'base_color': base_color,
                    'timestamp': timestamp,
                    'filepath': str(file)
                })
        except Exception as e:
            print(f"Error reading palette file {file}: {e}")
            continue
    
    return sorted(palettes, key=lambda x: x['timestamp'], reverse=True) 