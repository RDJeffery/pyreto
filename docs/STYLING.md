# Styling Guide

## Configuration Files

The application uses a `config.json` file to manage colors and display settings. The configuration is loaded from multiple locations in order of precedence:

1. `~/.config/palette-vault/config.json` (User config)
2. `/etc/palette-vault/config.json` (System config)
3. `./config.json` (Local config)

### Config Structure

```json
{
    "colors": {
        "background": "#1e1e2e",    // Main background color
        "accent": "#ff79c6",        // Accent color for headers and borders
        "hover": "#313244",         // Color for hover states
        "focus": "#45475a",         // Color for focused elements
        "text": "white"             // Main text color
    },
    "pywal": {
        "enabled": true,            // Enable/disable Pywal integration
        "background_key": "special.background",  // Pywal key for background
        "accent_key": "colors.color9",          // Pywal key for accent
        "hover_key": "colors.color8",           // Pywal key for hover states
        "focus_key": "colors.color10",          // Pywal key for focus states
        "text_key": "special.foreground",       // Pywal key for text color
        "header_key": "colors.color1"           // Pywal key for header color
    },
    "display": {
        "header_height": "3",       // Height of the header in lines
        "item_height": "3",         // Height of each color item in lines
        "padding": "1"              // Padding for elements in spaces
    }
}
```

## Pywal Integration

The application can automatically use colors from your Pywal theme. When enabled, it maps Pywal colors to different UI elements:

- Background: `special.background` (default: `#040D16`)
- Header: `colors.color1` (default: `#CC9A60`)
- Accent: `colors.color9` (default: `#CC9A60`)
- Hover: `colors.color8` (default: `#859796`)
- Focus: `colors.color10` (default: `#F6D175`)
- Text: `special.foreground` (default: `#bfd9d7`)

To enable Pywal integration, set `"enabled": true` in the `pywal` section of your config. You can customize which Pywal colors are used for each element by changing the corresponding keys.

## CSS Styling

The application's styling is defined in `app.css`. The CSS file is automatically updated with colors from your config when the app starts. The CSS uses a set of base colors that are replaced with your theme colors:

```css
/* Base colors that get replaced */
#1e1e2e    /* Background */
#ff79c6    /* Accent */
#313244    /* Hover */
#45475a    /* Focus */
white      /* Text */
#ff0000    /* Header */
```

### Available Style Properties

#### Screen (Main Container)
- `background`: Main background color
- `color`: Text color
- `border`: Border settings (currently disabled)
- `margin`: Margin settings (currently 0)
- `padding`: Padding settings (currently 0)
- `width`: Width (100%)
- `height`: Height (100%)
- `overflow`: Overflow behavior (hidden)

#### Header (#header)
- `background`: Header background color
- `color`: Header text color
- `padding`: Padding around header content
- `text-align`: Text alignment (center)
- `height`: Header height in lines
- `border`: Border settings (currently disabled)
- `margin`: Margin settings (currently 0)

#### ListView (Color List)
- `background`: List background color
- `border`: Border settings (currently disabled)
- `margin`: Margin settings (currently 0)
- `padding`: Padding settings (currently 0)
- `width`: Width (100%)
- `height`: Height (100%)
- `overflow-y`: Vertical scroll behavior (auto)
- `scrollbar-gutter`: Scrollbar space management (auto)

#### ColorItem (Individual Color Entries)
- `padding`: Padding around color items
- `height`: Height of each item in lines
- `border`: Border settings (currently disabled)
- `margin`: Margin settings (currently 0)

#### ColorItem States
- `:hover`: Hover state styling
  - `background`: Hover background color
- `:focus`: Focus state styling
  - `background`: Focus background color

#### Search Dialog
- `background`: Dialog background color
- `color`: Text color
- `border`: Border style and color
- `width`: Dialog width (80%)
- `height`: Dialog height (50%)
- `layer`: Overlay layer
- `offset`: Position offset
- `display`: Display mode
- `dock`: Docking position
- `margin`: Margin settings

#### Search Components
- `#search`: Search input field
  - `background`: Input background
  - `color`: Text color
  - `padding`: Padding
  - `height`: Height in lines
- `#search_results`: Results container
  - `background`: Background color
  - `height`: Height (1fr)

#### Toast Notifications
- `background`: Toast background color
- `color`: Text color
- `border`: Border style and color

#### Scrollbar
- `display`: Display mode (currently none)
- `width`: Width (0)
- `height`: Height (0)

## Common Issues

1. **Colors not updating**: 
   - Ensure your config file is in the correct location and has valid JSON syntax
   - Check that the CSS file is using the correct base colors that get replaced
   - Verify that Pywal colors are being loaded correctly (check debug output)

2. **Pywal colors not loading**: 
   - Check that Pywal is installed and has generated a colors file at `~/.cache/wal/colors.json`
   - Verify that `"enabled": true` is set in the Pywal config section
   - Check the debug output for any errors loading Pywal colors

3. **Style changes not applying**: 
   - Verify that the config values are being used correctly in the CSS
   - Check that the color mapping in `update_css_with_theme` includes all necessary colors
   - Ensure the CSS file is being properly updated with the new colors

## Missing Features (Planned)

The following styling features are planned for future releases:
- Font family customization
- Font size controls
- Text alignment options
- Border radius controls
- Animation settings
- Custom scrollbar styling
- More granular padding/margin controls
- Custom CSS file support
- Theme presets
- Additional Pywal color mappings
- Color opacity/transparency support
