#!/bin/bash
# Test script to validate branding installation and configuration

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Spec Kitty Branding Test Suite${NC}"
echo "=============================="
echo ""

# Test 1: Check if spec-kitty is installed
echo -e "${BLUE}[1/6]${NC} Checking spec-kitty installation..."
if command -v spec-kitty &> /dev/null; then
    SPEC_KITTY_VERSION=$(spec-kitty --version 2>&1 || echo "unknown")
    echo -e "${GREEN}✓${NC} spec-kitty found: $SPEC_KITTY_VERSION"
else
    echo -e "${RED}✗${NC} spec-kitty not found in PATH"
    exit 1
fi

# Test 2: Locate installation via find command
echo -e "${BLUE}[2/6]${NC} Locating spec-kitty-cli installation..."
PIPX_VENV=$(find ~/.local/pipx/venvs -name "spec-kitty-cli" -type d 2>/dev/null | head -1)
if [ -z "$PIPX_VENV" ]; then
    echo -e "${RED}✗${NC} Could not locate spec-kitty-cli pipx venv"
    exit 1
fi

VENV_PATH=$(find "$PIPX_VENV" -name "specify_cli" -type d | grep "site-packages/specify_cli$" | head -1)
if [ -z "$VENV_PATH" ]; then
    echo -e "${RED}✗${NC} Could not locate specify_cli package"
    exit 1
fi
echo -e "${GREEN}✓${NC} Found at: $VENV_PATH"

# Test 3: Check branding modules installed
echo -e "${BLUE}[3/6]${NC} Checking branding modules..."
BRANDING_LOADER="$VENV_PATH/branding_loader.py"
DASHBOARD_PATCH="$VENV_PATH/dashboard_patch.py"
BACKUP="$VENV_PATH/dashboard.py.original"

if [ -f "$BRANDING_LOADER" ]; then
    echo -e "${GREEN}✓${NC} branding_loader.py installed"
else
    echo -e "${RED}✗${NC} branding_loader.py not found"
    exit 1
fi

if [ -f "$DASHBOARD_PATCH" ]; then
    echo -e "${GREEN}✓${NC} dashboard_patch.py installed"
else
    echo -e "${RED}✗${NC} dashboard_patch.py not found"
    exit 1
fi

if [ -f "$BACKUP" ]; then
    echo -e "${GREEN}✓${NC} Original dashboard backup exists"
else
    echo -e "${YELLOW}⚠${NC}  No backup found (may not have been created yet)"
fi

# Test 4: Check __init__.py patch
echo -e "${BLUE}[4/6]${NC} Checking __init__.py patch..."
INIT_FILE="$VENV_PATH/__init__.py"
if grep -q "install_branding_patch" "$INIT_FILE" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Branding patch integrated in __init__.py"
else
    echo -e "${RED}✗${NC} Branding patch not found in __init__.py"
    exit 1
fi

# Test 5: Validate branding loader
echo -e "${BLUE}[5/6]${NC} Testing branding loader..."
PYTHON_TEST=$(python3 -c "
import sys
sys.path.insert(0, '$VENV_PATH')
try:
    from branding_loader import load_branding_config, DEFAULT_BRANDING
    config = load_branding_config()
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)

if [ "$PYTHON_TEST" = "OK" ]; then
    echo -e "${GREEN}✓${NC} branding_loader imports successfully"
else
    echo -e "${RED}✗${NC} branding_loader test failed: $PYTHON_TEST"
    exit 1
fi

# Test 6: Check for test project configuration
echo -e "${BLUE}[6/6]${NC} Checking test project configuration..."
TEST_CONFIG="/Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api/.kittify/branding.json"
if [ -f "$TEST_CONFIG" ]; then
    echo -e "${GREEN}✓${NC} Test branding.json exists at: $TEST_CONFIG"

    # Validate JSON
    if python3 -m json.tool "$TEST_CONFIG" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} JSON is valid"

        # Show project name
        PROJECT_NAME=$(python3 -c "import json; print(json.load(open('$TEST_CONFIG'))['projectName'])" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✓${NC} Project name: $PROJECT_NAME"
    else
        echo -e "${RED}✗${NC} Invalid JSON in branding.json"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC}  No test branding.json found (will use defaults)"
fi

echo ""
echo -e "${GREEN}All tests passed!${NC}"
echo ""
echo "Next steps:"
echo "  1. Navigate to: cd /Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api"
echo "  2. Start dashboard: spec-kitty dashboard"
echo "  3. Open browser to: http://127.0.0.1:9237"
echo "  4. Verify custom branding is applied"
echo ""
