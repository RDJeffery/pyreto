# 🎨 Pyreto - Your Color Palette Manager

An efficient terminal-based color palette manager that helps you search, and manage your color picker results.

## ✨ Features

- 🎯 **Quick Color Management**: Copy, favorite, and organize your colors
- 🔍 **Smart Search**: Live search through your color collection
- ⭐ **Favorites System**: Mark and filter your favorite colors
- 🎨 **Theme Integration**: Integration with Pywal for automatic theming
- ⌨️ **Keyboard-Driven**: Keyboard shortcuts for all operations
- 🎯 **Customizable**:  Styling options through CSS and config files

## 🎯 Color Picker Integration

Pyreto works seamlessly with color picker applications like Hyprpicker. It monitors and reads color data from JSON files that store hex codes and timestamps. For technical details about the integration and supported formats, see our [Integration Guide](docs/INTEGRATION.md).

## 🚀 Installation

### Arch Linux

1. Install the required dependencies:
```bash
sudo pacman -S python-pip python-pywal
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/pyreto.git
cd pyreto
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install the application system-wide:
```bash
sudo cp pyreto /usr/local/bin/
```

## 🎮 Usage

Run Pyreto from your terminal:
```bash
pyreto
```

### Keyboard Shortcuts

- `↑/↓`: Navigate colors
- `f`: Toggle favorite status
- `c`: Copy color to clipboard
- `h`: Toggle between All/Favorites view
- `s`: Toggle sort order
- Type in search bar to filter colors

## 🎨 Customization

Pyreto is customizable! Check out our [Styling Guide](docs/STYLING.md) for detailed information on:
- Theme configuration
- Pywal integration
- CSS customization
- Display settings
- And much more!

## 🛠️ Configuration

Configuration files are loaded from multiple locations in order of precedence:
1. `~/.config/pyreto/config.json` (User config)
2. `/etc/pyreto/config.json` (System config)
3. `./config.json` (Local config)

## 🐛 Troubleshooting

If you encounter any issues:
1. Check the debug output by enabling debug mode in your config
2. Verify your Pywal installation if using theme integration
3. Ensure all dependencies are properly installed
4. Check the [Styling Guide](docs/STYLING.md) for common issues and solutions

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual)
- Inspired by various color management tools
- Thanks to all contributors and users! 