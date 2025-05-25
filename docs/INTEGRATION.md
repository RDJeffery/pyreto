# Color Picker Integration Guide

## Supported Format

Pyreto reads color data from JSON files with the following structure:

```json
[
    {
        "hex": "#RRGGBB",
        "timestamp": 1234567890
    }
]
```

## Integration with Hyprpicker

1. Configure Hyprpicker to save colors in the supported JSON format
2. Set the output path in your Pyreto config:
```json
{
    "color_picker": {
        "input_file": "~/.config/hyprpicker/colors.json"
    }
}
```

## Technical Details

- Colors are stored with hex codes (6-digit RGB)
- Timestamps are Unix timestamps (seconds since epoch)
- File is monitored for changes and automatically reloaded
- Duplicate colors are automatically handled
- Colors are sorted by timestamp by default

## Supported Color Pickers

- Hyprpicker (with JSON output)
- Other pickers that output compatible JSON format

## Custom Integration

To integrate with other color pickers:
1. Ensure output is in the supported JSON format
2. Configure the input file path in Pyreto's config
3. Restart Pyreto to load the new configuration 