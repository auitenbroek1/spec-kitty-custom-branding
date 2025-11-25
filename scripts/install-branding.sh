#!/bin/bash
# Install custom branding support for Spec Kitty dashboard
# This script patches the installed spec-kitty-cli to support branding configuration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Spec Kitty Branding Installer${NC}"
echo "================================"
echo ""

# Find spec-kitty installation
SPEC_KITTY_PATH=$(which spec-kitty 2>/dev/null || true)

if [ -z "$SPEC_KITTY_PATH" ]; then
    echo -e "${RED}Error: spec-kitty not found in PATH${NC}"
    echo "Please install spec-kitty-cli first:"
    echo "  pipx install spec-kitty-cli"
    exit 1
fi

echo -e "${GREEN}✓${NC} Found spec-kitty at: $SPEC_KITTY_PATH"

# Find the pipx venv directory by searching for spec-kitty-cli
PIPX_VENV=$(find ~/.local/pipx/venvs -name "spec-kitty-cli" -type d 2>/dev/null | head -1)

if [ -z "$PIPX_VENV" ]; then
    echo -e "${RED}Error: Could not locate spec-kitty-cli pipx venv${NC}"
    echo "Please ensure spec-kitty-cli is installed: pipx install spec-kitty-cli"
    exit 1
fi

# Find the Python package directory
VENV_PATH=$(find "$PIPX_VENV" -name "specify_cli" -type d | grep "site-packages/specify_cli$" | head -1)

if [ -z "$VENV_PATH" ]; then
    echo -e "${RED}Error: Could not locate specify_cli package${NC}"
    exit 1
fi

DASHBOARD_PATH="$VENV_PATH/dashboard.py"

if [ ! -f "$DASHBOARD_PATH" ]; then
    echo -e "${RED}Error: Dashboard file not found at: $DASHBOARD_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Found dashboard.py at: $DASHBOARD_PATH"

# Create backup
BACKUP_PATH="${DASHBOARD_PATH}.original"
if [ ! -f "$BACKUP_PATH" ]; then
    echo "Creating backup of original dashboard.py..."
    cp "$DASHBOARD_PATH" "$BACKUP_PATH"
    echo -e "${GREEN}✓${NC} Backup created: $BACKUP_PATH"
else
    echo -e "${YELLOW}⚠${NC}  Backup already exists, skipping"
fi

# Copy branding modules
BRANDING_MODULES_DIR="$VENV_PATH"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CUSTOM_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "Installing branding modules..."

cp "$CUSTOM_DIR/branding_loader.py" "$BRANDING_MODULES_DIR/"
echo -e "${GREEN}✓${NC} Installed branding_loader.py"

cp "$CUSTOM_DIR/dashboard_patch.py" "$BRANDING_MODULES_DIR/"
echo -e "${GREEN}✓${NC} Installed dashboard_patch.py"

# Patch the dashboard __init__.py to apply branding on startup
INIT_FILE="$BRANDING_MODULES_DIR/__init__.py"

if ! grep -q "install_branding_patch" "$INIT_FILE" 2>/dev/null; then
    echo "" >> "$INIT_FILE"
    echo "# Apply custom branding support" >> "$INIT_FILE"
    echo "try:" >> "$INIT_FILE"
    echo "    from .dashboard_patch import install_branding_patch" >> "$INIT_FILE"
    echo "    install_branding_patch()" >> "$INIT_FILE"
    echo "except Exception as e:" >> "$INIT_FILE"
    echo "    pass  # Branding patch optional" >> "$INIT_FILE"

    echo -e "${GREEN}✓${NC} Patched __init__.py to load branding on startup"
else
    echo -e "${YELLOW}⚠${NC}  Branding patch already present in __init__.py"
fi

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "To customize your branding:"
echo "  1. Create .kittify/branding.json in your project directory"
echo "  2. Use the template at: $CUSTOM_DIR/templates/branding.json"
echo "  3. Restart the dashboard to see your changes"
echo ""
echo "To restore original dashboard:"
echo "  cp $BACKUP_PATH $DASHBOARD_PATH"
echo ""
