# YGScript VSCode Extension

Complete language support for YGScript programming language in VS Code.

## Features

✨ **Syntax Highlighting** - Full syntax highlighting for YGScript code with proper token recognition
🎨 **File Icons** - Custom icons for `.yg` files in the file explorer
🔍 **Real-time Error Checking** - Automatic syntax and parse error detection as you type
▶️ **Run YGScript Files** - Execute YGScript files directly from the editor (Ctrl+Shift+R)
📝 **Language Configuration** - Auto-completion, bracket matching, and more

## Installation

### From VS Code Marketplace
1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "ygscript"
3. Click Install

### Manual Installation
1. Clone the repository
2. Copy the extension folder to `~/.vscode/extensions/ygscript-1.0.0/`
3. Restart VS Code

## Usage

### Running YGScript Files
- **Keyboard Shortcut**: `Ctrl+Shift+R` (with an open .yg file)
- **Command Palette**: Search for "Run YGScript File"
- Output appears in the YGScript output channel

### File Format
Create files with `.yg` extension to get full language support:
```ygscript
show("Hello from YGScript!")
```

## Syntax Highlighting Scopes

The extension includes comprehensive syntax highlighting for:
- **Keywords**: if, elif, else, for, while, do, agin, fac, yield, return, import, break, continue
- **Types**: int, float, bool, string, null, array, map
- **Operators**: Arithmetic (+, -, *, /, %, ^), Comparison (==, !=, <, <=, >, >=), Logical (&&, ||, !)
- **Built-in Functions**: show, input, len, type, int, float, str, abs, min, max, round, floor, ceil
- **Comments**: Single-line (//) and multi-line (/* */)
- **Strings**: Single and double quoted strings with escape sequences
- **Numbers**: Integers, floats, and scientific notation

## Configuration

### YGScript Binary Path
If the extension cannot find the YGScript compiler, update the path in `extension.js`:
```javascript
const compilerPath = "path/to/ygscript.exe"; // or .sh on Unix
```

### Editor Settings
In VS Code settings.json:
```json
{
  "editor.defaultFormatter": "YGStudio.ygscript",
  "[ygscript]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.formatOnSave": true
  }
}
```

## File Icons

The extension provides:
- `.yg` file icon - Custom YGScript icon with distinctive styling
- Theme support - Works with both light and dark VS Code themes
- Explorer integration - Icons appear in the file tree

## Error Checking

Real-time error detection shows:
- **Syntax Errors** - Tokenization failures
- **Parse Errors** - Grammar violations
- **Type Errors** - Type mismatches (when available)

Errors are displayed with:
- Line and column numbers
- Error message
- Red underline in the editor

## Troubleshooting

### Extension not activating
- Check that you have `.yg` files open
- Verify the file language is set to "YGScript"
- Restart VS Code

### Run command not working
- Ensure YGScript compiler is installed
- Check the compiler path in `extension.js`
- Verify the `.yg` file is saved (or use Ctrl+S)

### Icons not showing
- Reload VS Code window (Ctrl+Shift+P → Reload Window)
- Check VS Code version is 1.74.0 or newer

### Error checking too slow
- Increase debounce timeout in `extension.js` (default: 800ms)
- Use simpler files for testing

## Support

For issues or questions:
- GitHub Issues: https://github.com/YGStudio/ygscript
- Documentation: See README.md in the YGScript project

## License

MIT License - See LICENSE file for details
