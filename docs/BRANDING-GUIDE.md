# Spec Kitty Custom Branding Guide

This guide explains how to customize the Spec Kitty dashboard with your own branding, including logos, colors, and project names.

## Quick Start

1. **Install branding support:**
   ```bash
   cd /Users/aaronuitenbroek/hive-projects/SpecKitty/spec-kitty-custom
   ./scripts/install-branding.sh
   ```

2. **Create your branding configuration:**
   ```bash
   cd your-project-directory
   mkdir -p .kittify
   cp /path/to/spec-kitty-custom/templates/branding.json .kittify/
   ```

3. **Edit `.kittify/branding.json` with your branding:**
   ```json
   {
     "projectName": "My Awesome Project",
     "shortName": "MyProject",
     "welcomeMessage": "Welcome to My Awesome Project!",
     "logoPath": "/static/my-logo.png",
     "faviconPath": "/static/my-favicon.png",
     "colors": {
       "primary": "#0066CC",
       "secondary": "#00CC66",
       "accent": "#FFAA00",
       "background": "#FFFFFF"
     }
   }
   ```

4. **Add your logo files:**
   ```bash
   cp your-logo.png .kittify/static/my-logo.png
   cp your-favicon.png .kittify/static/my-favicon.png
   ```

5. **Restart the dashboard:**
   ```bash
   spec-kitty dashboard
   ```

## Configuration Reference

### Required Fields

- **projectName** (string): Full display name for your project
  - Example: `"Energy Monitor API"`
  - Used in: Page title, header, welcome message

### Optional Fields

- **shortName** (string): Abbreviated name for compact displays
  - Default: Same as `projectName`
  - Example: `"EnergyAPI"`
  - Used in: Header h1 element

- **welcomeMessage** (string): Welcome message on dashboard
  - Default: `"Welcome to Spec Kitty!"`
  - Example: `"Welcome to Energy Monitoring!"`

- **logoPath** (string): Path to your logo image
  - Default: `"/static/spec-kitty.png"`
  - Supports: Relative paths to `.kittify/` or absolute URLs
  - Recommended size: 60x60px (will be contained)
  - Example: `"/static/my-logo.png"`

- **faviconPath** (string): Path to your favicon
  - Default: `"/static/spec-kitty.png"`
  - Supports: Relative paths to `.kittify/` or absolute URLs
  - Format: PNG recommended
  - Example: `"/static/favicon.png"`

### Color Customization

The **colors** object allows you to customize the color scheme:

```json
{
  "colors": {
    "primary": "#A7C7E7",      // Main brand color (headers, accents)
    "secondary": "#7BB661",    // Secondary brand color (buttons, links)
    "accent": "#FFF275",       // Accent color (highlights)
    "background": "#FFFDF7"    // Background color
  }
}
```

Colors must be specified in hex format (e.g., `#A7C7E7`).

### Footer Customization

```json
{
  "footer": {
    "text": "Powered by My Company",
    "link": "https://mycompany.com"
  }
}
```

- **text** (string): Footer text to display
- **link** (string, optional): URL to link the footer text to

## Examples

### Minimal Configuration

```json
{
  "projectName": "My Project"
}
```

This uses all defaults except the project name.

### Complete Configuration

```json
{
  "projectName": "Energy Monitor API",
  "shortName": "Energy API",
  "welcomeMessage": "Welcome to Real-Time Energy Monitoring!",
  "logoPath": "/static/energy-logo.png",
  "faviconPath": "/static/energy-favicon.ico",
  "colors": {
    "primary": "#1E40AF",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "background": "#F9FAFB"
  },
  "footer": {
    "text": "© 2025 Energy Solutions Inc.",
    "link": "https://energysolutions.example.com"
  }
}
```

### Corporate Branding

```json
{
  "projectName": "Acme Corp Specifications",
  "shortName": "Acme Specs",
  "welcomeMessage": "Acme Specification Management",
  "logoPath": "https://cdn.acmecorp.com/logo.svg",
  "faviconPath": "https://cdn.acmecorp.com/favicon.png",
  "colors": {
    "primary": "#E31837",
    "secondary": "#001F3F",
    "accent": "#FFD700",
    "background": "#FFFFFF"
  },
  "footer": {
    "text": "Acme Corporation - Trusted since 1949",
    "link": "https://acmecorp.com"
  }
}
```

## Static Assets

### Logo Requirements

- **Format**: PNG, SVG, or JPG
- **Recommended size**: 60x60px (square)
- **Max size**: 200x200px (will be scaled down)
- **Location**: Place in `.kittify/static/` directory
- **Transparency**: Supported (PNG/SVG)

### Favicon Requirements

- **Format**: PNG or ICO
- **Size**: 16x16px or 32x32px
- **Location**: Place in `.kittify/static/` directory

### File Organization

```
your-project/
├── .kittify/
│   ├── branding.json          # Your branding configuration
│   └── static/                # Your custom assets
│       ├── my-logo.png
│       ├── my-favicon.png
│       └── other-assets.png
```

## Validation

Validate your branding configuration:

```bash
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '/path/to/spec-kitty-custom')
from branding_loader import validate_branding_config

valid, error = validate_branding_config(Path('.kittify/branding.json'))
if valid:
    print('✓ Configuration is valid')
else:
    print(f'✗ Configuration error: {error}')
"
```

## Troubleshooting

### Dashboard shows default "Spec Kitty" branding

1. Check that `.kittify/branding.json` exists:
   ```bash
   ls -la .kittify/branding.json
   ```

2. Validate your JSON syntax:
   ```bash
   python3 -m json.tool .kittify/branding.json
   ```

3. Restart the dashboard:
   ```bash
   # Stop the current dashboard (Ctrl+C)
   spec-kitty dashboard
   ```

### Logo or favicon not showing

1. Check file exists:
   ```bash
   ls -la .kittify/static/your-logo.png
   ```

2. Verify path in branding.json matches file location

3. Check file permissions:
   ```bash
   chmod 644 .kittify/static/*.png
   ```

### Colors not applying

1. Ensure hex colors start with `#`
2. Use 6-digit hex format (e.g., `#A7C7E7`, not `#ACE`)
3. Check for syntax errors in JSON

### Restore original branding

```bash
# Find your spec-kitty installation
VENV_PATH=$(pipx list | grep -A1 "spec-kitty-cli" | grep "location:" | awk '{print $2}')

# Restore from backup
cp "$VENV_PATH/specify_cli/dashboard.py.original" "$VENV_PATH/specify_cli/dashboard.py"

# Restart dashboard
spec-kitty dashboard
```

## Uninstallation

To remove branding support:

```bash
# Find installation path
VENV_PATH=$(pipx list | grep -A1 "spec-kitty-cli" | grep "location:" | awk '{print $2}')

# Restore original dashboard
cp "$VENV_PATH/specify_cli/dashboard.py.original" "$VENV_PATH/specify_cli/dashboard.py"

# Remove branding modules
rm "$VENV_PATH/specify_cli/branding_loader.py"
rm "$VENV_PATH/specify_cli/dashboard_patch.py"

# Edit __init__.py to remove branding import (manual step)
# Remove the lines added by install-branding.sh
```

## Support

For issues or questions:

1. Check this guide first
2. Validate your configuration file
3. Check the console output for error messages
4. Restore from backup if needed

## Advanced Usage

### Programmatic Configuration

```python
from pathlib import Path
from branding_loader import create_branding_file

# Create branding config programmatically
create_branding_file(
    output_path=Path('.kittify/branding.json'),
    project_name="My Project",
    shortName="MyProj",
    colors={
        "primary": "#0066CC",
        "secondary": "#00CC66"
    }
)
```

### Environment-Specific Branding

Create different configurations for different environments:

```bash
# Development
cp .kittify/branding.dev.json .kittify/branding.json

# Production
cp .kittify/branding.prod.json .kittify/branding.json
```

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
- name: Configure branding
  run: |
    mkdir -p .kittify/static
    cp branding/${{ env.ENVIRONMENT }}.json .kittify/branding.json
    cp assets/logo.png .kittify/static/
```
