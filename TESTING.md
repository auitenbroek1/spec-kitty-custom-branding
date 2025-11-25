# Branding Customization Testing Guide

This guide provides step-by-step instructions for testing the Spec Kitty custom branding system.

## Prerequisites

- spec-kitty-cli installed via pipx
- Branding modules installed (run `./scripts/install-branding.sh` if not done)

## Quick Test: Existing Energy Monitor API Project

### Option 1: Test with Current Project (Recommended)

This uses your existing `energy-monitor-api` project that already has a `.kittify` directory:

```bash
# 1. Navigate to the energy monitor API project
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api

# 2. Verify branding.json was created
cat .kittify/branding.json

# 3. Start the dashboard
spec-kitty dashboard

# 4. Open browser to http://127.0.0.1:9237 (or the port shown in terminal)

# Expected Results:
# - Page title: "Energy Monitor API Dashboard" (not "Spec Kitty Dashboard")
# - Header text: "Energy API" (not "Spec Kitty")
# - Welcome message: "Welcome to Real-Time Energy Monitoring!"
# - Color scheme: Blue/green/orange instead of original pastels
# - Footer: "Energy Monitor API - Real-time monitoring system"
```

### Option 2: Test with New Project

Create a fresh test project to verify the system works from scratch:

```bash
# 1. Create new test project
mkdir -p ~/test-spec-kitty-branding
cd ~/test-spec-kitty-branding

# 2. Initialize spec-kitty
spec-kitty init

# 3. Create custom branding
mkdir -p .kittify/static
cat > .kittify/branding.json << 'EOF'
{
  "projectName": "Test Branding Project",
  "shortName": "TestBrand",
  "welcomeMessage": "Welcome to Branding Test!",
  "logoPath": "/static/spec-kitty.png",
  "faviconPath": "/static/spec-kitty.png",
  "colors": {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    "accent": "#FFE66D",
    "background": "#F7F7F7"
  },
  "footer": {
    "text": "Custom Footer Test",
    "link": "https://example.com"
  }
}
EOF

# 4. Start dashboard
spec-kitty dashboard

# 5. Open browser to http://127.0.0.1:9237

# Expected Results:
# - Page title: "Test Branding Project Dashboard"
# - Header: "TestBrand"
# - Welcome: "Welcome to Branding Test!"
# - Colors: Red/teal/yellow scheme
# - Footer: Clickable link to example.com
```

## Detailed Verification Steps

### 1. Visual Inspection Checklist

Open the dashboard and verify:

**Header Section:**
- [ ] Logo displays correctly (default or custom)
- [ ] Project name matches `shortName` from config
- [ ] Header colors reflect `colors.primary`

**Page Title:**
- [ ] Browser tab title shows `{projectName} Dashboard`
- [ ] Favicon displays (check browser tab icon)

**Welcome Page:**
- [ ] Welcome message matches `welcomeMessage` from config
- [ ] Background color matches `colors.background`

**Navigation & Content:**
- [ ] Sidebar buttons use `colors.secondary` for active state
- [ ] Accent color appears in highlights and borders

**Footer (if configured):**
- [ ] Footer text displays at bottom of page
- [ ] Footer link is clickable (if URL provided)

### 2. Configuration Validation Test

Test the validation system:

```bash
# Navigate to custom branding directory
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/spec-kitty-custom

# Test valid configuration
python3 -c "
from pathlib import Path
from branding_loader import validate_branding_config
import sys

config_path = Path('/Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api/.kittify/branding.json')
valid, error = validate_branding_config(config_path)

if valid:
    print('✓ Configuration is valid')
    sys.exit(0)
else:
    print(f'✗ Configuration error: {error}')
    sys.exit(1)
"

# Test invalid configuration (intentionally break JSON)
echo '{invalid json}' > /tmp/test-invalid.json
python3 -c "
from pathlib import Path
from branding_loader import validate_branding_config

valid, error = validate_branding_config(Path('/tmp/test-invalid.json'))
print(f'Expected failure: {error}')
"
```

### 3. Fallback Behavior Test

Test that the system gracefully falls back to defaults:

```bash
# 1. Temporarily rename branding.json
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api
mv .kittify/branding.json .kittify/branding.json.backup

# 2. Start dashboard
spec-kitty dashboard

# Expected: Dashboard shows default "Spec Kitty" branding

# 3. Restore branding
mv .kittify/branding.json.backup .kittify/branding.json

# 4. Restart dashboard
# Expected: Custom branding returns
```

### 4. Color Scheme Test

Test different color configurations:

```bash
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api

# Backup current config
cp .kittify/branding.json .kittify/branding.json.backup

# Test 1: Dark theme
cat > .kittify/branding.json << 'EOF'
{
  "projectName": "Energy Monitor API - Dark",
  "shortName": "Energy API",
  "colors": {
    "primary": "#1F2937",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "background": "#111827"
  }
}
EOF

# Start dashboard and check dark colors
spec-kitty dashboard

# Test 2: Light theme
cat > .kittify/branding.json << 'EOF'
{
  "projectName": "Energy Monitor API - Light",
  "shortName": "Energy API",
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#8B5CF6",
    "accent": "#EC4899",
    "background": "#FFFFFF"
  }
}
EOF

# Start dashboard and check light colors
spec-kitty dashboard

# Restore original
mv .kittify/branding.json.backup .kittify/branding.json
```

### 5. Logo and Asset Test

Test custom logo files (requires image files):

```bash
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/energy-monitor-api

# Create test logo placeholder (or use real image)
# If you have a logo:
# cp /path/to/your-logo.png .kittify/static/custom-logo.png

# Update branding to use custom logo
cat > .kittify/branding.json << 'EOF'
{
  "projectName": "Energy Monitor API",
  "shortName": "Energy API",
  "logoPath": "/static/custom-logo.png",
  "faviconPath": "/static/custom-logo.png"
}
EOF

# Start dashboard
spec-kitty dashboard

# Check that custom logo appears in header
# If file doesn't exist, you should see broken image icon
```

## Automated Test Suite

Run the complete test suite:

```bash
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/spec-kitty-custom
./scripts/test-branding.sh
```

This will verify:
1. spec-kitty installation
2. pipx venv location
3. Branding modules installed
4. __init__.py patched correctly
5. Python imports work
6. Test configuration exists and is valid

## Troubleshooting Test Issues

### Dashboard shows default "Spec Kitty" branding

**Check 1: Verify branding.json exists**
```bash
ls -la .kittify/branding.json
cat .kittify/branding.json
```

**Check 2: Validate JSON syntax**
```bash
python3 -m json.tool .kittify/branding.json
```

**Check 3: Check console output**
When starting the dashboard, look for:
- "✓ Branding patch installed successfully"
- Any error messages about loading branding

**Check 4: Verify you're in correct directory**
```bash
pwd  # Should be in the project directory with .kittify/
ls -la .kittify/
```

### Colors not applying

**Issue**: Custom colors don't show in dashboard

**Fix**: Verify hex color format:
```bash
# Colors must start with # and be 6 digits
# ✓ Good: "#1E40AF"
# ✗ Bad: "1E40AF", "#1E4", "blue"
```

### Logo/favicon not showing

**Issue**: Custom logo doesn't display

**Fixes**:
1. Verify file exists:
```bash
ls -la .kittify/static/your-logo.png
```

2. Check file permissions:
```bash
chmod 644 .kittify/static/*.png
```

3. Verify path in branding.json:
```json
{
  "logoPath": "/static/your-logo.png"  // Must match filename
}
```

### Import errors in console

**Issue**: Python import errors when starting dashboard

**Fix**: Reinstall branding modules:
```bash
cd /Users/aaronuitenbroek/hive-projects/SpecKitty/spec-kitty-custom
./scripts/install-branding.sh
```

## Uninstall for Testing

If you need to test with vanilla spec-kitty:

```bash
# Find installation path
VENV_PATH=$(pipx list | grep -A1 "spec-kitty-cli" | grep "location:" | awk '{print $2}')

# Restore original (keeps branding modules but disables them)
cp "$VENV_PATH/specify_cli/dashboard.py.original" "$VENV_PATH/specify_cli/dashboard.py"

# Restart dashboard
spec-kitty dashboard

# Should show default Spec Kitty branding
```

To re-enable:
```bash
./scripts/install-branding.sh
```

## Test Results Documentation

After testing, document your results:

```bash
# Create test report
cat > /Users/aaronuitenbroek/hive-projects/SpecKitty/spec-kitty-custom/TEST-RESULTS.md << 'EOF'
# Branding Test Results

**Date**: $(date)
**Tester**: Your Name
**spec-kitty version**: $(spec-kitty --version 2>&1)

## Test Summary

- [ ] Installation successful
- [ ] Branding loads correctly
- [ ] Colors apply properly
- [ ] Logo displays correctly
- [ ] Welcome message customized
- [ ] Footer appears (if configured)
- [ ] Fallback to defaults works
- [ ] JSON validation works

## Issues Found

List any issues encountered...

## Screenshots

(Add screenshots showing before/after branding)
EOF
```

## Next Steps After Testing

If all tests pass:

1. ✅ Customize branding.json for your actual project
2. ✅ Add your company logo
3. ✅ Choose your brand colors
4. ✅ Share the system with your team

If tests fail:
1. Review error messages
2. Check troubleshooting section
3. Verify installation steps
4. Consider opening an issue if problem persists
