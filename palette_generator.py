import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import colorsys
import subprocess
import logging

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

def create_palettes_readme() -> None:
    """Create a README.md file in the Palettes directory explaining the format."""
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    readme_path = palettes_dir / "README.md"
    
    readme_content = """# Pyreto Color Palettes

This directory contains color palettes generated by Pyreto. Each palette is saved as a Markdown file with the following format:

## File Naming
Palettes are named using the pattern: `palette_[HEXCOLOR]_[TIMESTAMP].md`
Example: `palette_FF5733_20240314_153045.md`

## Palette Contents
Each palette file contains:
- Base color with visual swatch
- Analogous colors (adjacent on the color wheel)
- Complementary colors (opposite on the color wheel)
- Triadic colors (three colors equally spaced)
- Split complementary colors
- Tetradic colors (four colors in two complementary pairs)

## Viewing Palettes
You can view these files using any Markdown viewer. The files include:
- Color swatches using placeholder.com
- Hex color codes
- Generation timestamp
- Palette name

## Opening in Pyreto
You can view these palettes directly in Pyreto by:
1. Opening Pyreto
2. Pressing 'v' to view saved palettes
3. Selecting a palette to view its details

## Opening Directory
You can open this directory in your file manager by:
1. Opening Pyreto
2. Pressing 'o' to open the Palettes directory
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)

def create_color_block(color: str) -> str:
    """Create an ASCII art block of the given color."""
    block = []
    for _ in range(size):
        block.append("█")
    return "\n".join(block)

def create_code_example(color: str) -> str:
    """Create code examples for the given color."""
    return f"""```css
/* CSS Example */
.color-example {{
    color: {color};
    background-color: {color}33;  /* 20% opacity */
    border: 2px solid {color};
}}

/* SCSS Example */
$primary-color: {color};
.element {{
    color: $primary-color;
    &:hover {{
        background-color: lighten($primary-color, 10%);
    }}
}}

/* Tailwind Example */
<div class="text-[{color}] bg-[{color}]/20 border-2 border-[{color}]">
    Colored content
</div>
```"""

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
```
{create_color_block(base_color)}
```
`{base_color}`

{create_code_example(base_color)}

## Analogous Colors
These colors are adjacent on the color wheel, creating a harmonious and cohesive look.

{chr(10).join(f'''
### {color}
```
{create_color_block(color)}
```
`{color}`
{create_code_example(color)}
''' for color in analogous)}

## Complementary Colors
These colors are opposite on the color wheel, creating high contrast and visual impact.

{chr(10).join(f'''
### {color}
```
{create_color_block(color)}
```
`{color}`
{create_code_example(color)}
''' for color in complementary)}

## Triadic Colors
These colors are equally spaced on the color wheel, creating a balanced and vibrant palette.

{chr(10).join(f'''
### {color}
```
{create_color_block(color)}
```
`{color}`
{create_code_example(color)}
''' for color in triadic)}

## Split Complementary Colors
This scheme uses a base color and two colors adjacent to its complement, offering high contrast but less tension than complementary colors.

{chr(10).join(f'''
### {color}
```
{create_color_block(color)}
```
`{color}`
{create_code_example(color)}
''' for color in split_complementary)}

## Tetradic Colors
This scheme uses four colors arranged into two complementary pairs, offering rich color possibilities.

{chr(10).join(f'''
### {color}
```
{create_color_block(color)}
```
`{color}`
{create_code_example(color)}
''' for color in tetradic)}

## Usage Tips
- Use the base color as your primary brand color
- Analogous colors work well for gradients and subtle variations
- Complementary colors are great for call-to-action elements
- Triadic colors offer balanced contrast while maintaining harmony
- Split complementary colors provide high contrast with less tension
- Tetradic colors offer rich possibilities for complex designs

## Color Theory Notes
- **Hue**: The pure color (position on the color wheel)
- **Saturation**: The intensity or purity of the color
- **Value**: The brightness or darkness of the color
- **Complementary**: Colors opposite on the wheel create maximum contrast
- **Analogous**: Colors next to each other create harmony
- **Triadic**: Three colors equally spaced create balance
- **Split Complementary**: A base color and two colors adjacent to its complement
- **Tetradic**: Four colors arranged into two complementary pairs
"""
    
    # Create Pyreto directory in Documents if it doesn't exist
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    palettes_dir.mkdir(parents=True, exist_ok=True)
    
    # Create README if it doesn't exist
    if not (palettes_dir / "README.md").exists():
        create_palettes_readme()
    
    # Save the markdown file
    filename = f"palette_{base_color.lstrip('#')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = palettes_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(md_content)
    
    return str(filepath)

def open_palettes_directory() -> None:
    """Open the Palettes directory in the default file manager."""
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    if not palettes_dir.exists():
        palettes_dir.mkdir(parents=True, exist_ok=True)
        create_palettes_readme()
    
    # Use xdg-open on Linux, open on macOS, or explorer on Windows
    if subprocess.run(['which', 'xdg-open'], capture_output=True).returncode == 0:
        subprocess.run(['xdg-open', str(palettes_dir)])
    elif subprocess.run(['which', 'open'], capture_output=True).returncode == 0:
        subprocess.run(['open', str(palettes_dir)])
    else:
        subprocess.run(['explorer', str(palettes_dir)])

def list_saved_palettes() -> List[Dict]:
    """List all saved palettes with their metadata."""
    logger = logging.getLogger(__name__)
    palettes_dir = Path.home() / "Documents" / "Pyreto" / "Palettes"
    logger.debug(f"Looking for palettes in: {palettes_dir}")
    
    if not palettes_dir.exists():
        logger.debug(f"Palettes directory does not exist: {palettes_dir}")
        return []
    
    logger.debug(f"Found palettes directory, scanning for files...")
    palette_files = list(palettes_dir.glob("palette_*.md"))
    logger.debug(f"Found {len(palette_files)} palette files")
    
    palettes = []
    for file in palette_files:
        try:
            logger.debug(f"Processing palette file: {file}")
            logger.debug(f"Filename parts: {file.stem.split('_')}")
            
            with open(file, 'r') as f:
                content = f.read()
                
                # Debug the content
                logger.debug(f"File content first line: {content.split('\n')[0]}")
                
                # Extract base color from filename
                try:
                    base_color = f"#{file.stem.split('_')[1]}"
                    logger.debug(f"Extracted base color: {base_color}")
                except IndexError as e:
                    logger.error(f"Failed to extract base color from filename {file}: {e}")
                    continue
                
                # Extract timestamp from filename - try multiple formats
                try:
                    timestamp_str = file.stem.split('_')[2]
                    logger.debug(f"Raw timestamp string: {timestamp_str}")
                    
                    # Try different timestamp formats
                    timestamp_formats = [
                        "%Y%m%d_%H%M%S",  # Original format: 20240314_153045
                        "%Y%m%d",         # Just date: 20240314
                        "%Y-%m-%d_%H%M%S", # With dashes: 2024-03-14_153045
                        "%Y-%m-%d"        # Just date with dashes: 2024-03-14
                    ]
                    
                    timestamp = None
                    for fmt in timestamp_formats:
                        try:
                            timestamp = datetime.strptime(timestamp_str, fmt)
                            logger.debug(f"Successfully parsed timestamp using format: {fmt}")
                            break
                        except ValueError:
                            continue
                    
                    if timestamp is None:
                        # If no format matches, use file's modification time
                        timestamp = datetime.fromtimestamp(file.stat().st_mtime)
                        logger.debug(f"Using file modification time as timestamp: {timestamp}")
                    
                except (IndexError, ValueError) as e:
                    logger.error(f"Failed to extract timestamp from filename {file}: {e}")
                    # Use file's modification time as fallback
                    timestamp = datetime.fromtimestamp(file.stat().st_mtime)
                    logger.debug(f"Using file modification time as fallback: {timestamp}")
                
                # Extract palette name from content
                try:
                    name = content.split('\n')[0].lstrip('# ')
                    logger.debug(f"Extracted name: {name}")
                except Exception as e:
                    logger.error(f"Failed to extract name from content: {e}")
                    name = f"Palette from {base_color}"
                
                palette_info = {
                    'name': name,
                    'base_color': base_color,
                    'timestamp': timestamp,
                    'filepath': str(file)
                }
                logger.debug(f"Successfully processed palette: {palette_info}")
                palettes.append(palette_info)
                
        except Exception as e:
            logger.error(f"Error reading palette file {file}: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            continue
    
    sorted_palettes = sorted(palettes, key=lambda x: x['timestamp'], reverse=True)
    logger.debug(f"Returning {len(sorted_palettes)} sorted palettes")
    return sorted_palettes 