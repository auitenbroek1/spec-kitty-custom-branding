#!/usr/bin/env python3
"""
Branding configuration loader for Spec Kitty dashboard customization.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_BRANDING = {
    "projectName": "Spec Kitty",
    "shortName": "Spec Kitty",
    "welcomeMessage": "Welcome to Spec Kitty!",
    "logoPath": "/static/spec-kitty.png",
    "faviconPath": "/static/spec-kitty.png",
    "colors": {
        "primary": "#B8860B",      # hive-gold-dark  (text on light)
        "secondary": "#DAA520",    # hive-gold (accents)
        "accent": "#FFBF00",       # honey-bright (highlights)
        "background": "#FFFFFF",   # white
        "sidebar": "#FFF9F0",      # warm off-white
        "text": "#111827",         # almost black
        "textSecondary": "#4B5563", # medium gray
        "border": "#E5E7EB"        # light gray border
    },
    "footer": {
        "text": "Powered by Spec Kitty",
        "link": ""
    }
}


def load_branding_config(kittify_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load branding configuration from .kittify/branding.json.

    Args:
        kittify_dir: Path to .kittify directory. If None, searches from current directory.

    Returns:
        Dictionary with branding configuration. Falls back to defaults if not found.
    """
    if kittify_dir is None:
        # Search for .kittify directory starting from current directory
        current = Path.cwd()
        while current != current.parent:
            kittify_candidate = current / ".kittify"
            if kittify_candidate.exists() and kittify_candidate.is_dir():
                kittify_dir = kittify_candidate
                break
            current = current.parent

        if kittify_dir is None:
            # Not found, use defaults
            return DEFAULT_BRANDING.copy()

    branding_file = kittify_dir / "branding.json"

    if not branding_file.exists():
        return DEFAULT_BRANDING.copy()

    try:
        with open(branding_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Merge with defaults to ensure all required fields exist
        branding = DEFAULT_BRANDING.copy()
        branding.update(config)

        # Ensure nested dictionaries are also merged
        if "colors" in config:
            branding["colors"].update(config["colors"])
        if "footer" in config:
            branding["footer"].update(config["footer"])

        return branding

    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to load branding config: {e}")
        return DEFAULT_BRANDING.copy()


def get_css_variables(branding: Dict[str, Any]) -> str:
    """
    Generate CSS custom properties from branding configuration.

    Args:
        branding: Branding configuration dictionary

    Returns:
        CSS :root selector with custom properties
    """
    colors = branding.get("colors", DEFAULT_BRANDING["colors"])

    return f"""
        :root {{
            /* ==================== */
            /* Primary Brand Colors */
            /* ==================== */
            --hive-gold-dark: {colors.get('primary', '#B8860B')};     /* Dark gold for text on light */
            --hive-gold: {colors.get('secondary', '#DAA520')};        /* Medium gold for accents */
            --honey-bright: {colors.get('accent', '#FFBF00')};        /* Bright gold for highlights */
            
            /* Legacy color names for backwards compatibility */
            --baby-blue: {colors.get('primary', '#B8860B')};
            --grassy-green: {colors.get('secondary', '#DAA520')};
            --sunny-yellow: {colors.get('accent', '#FFBF00')};
            
            /* ==================== */
            /* Background Colors    */
            /* ==================== */
            --bg-white: {colors.get('background', '#FFFFFF')};        /* Pure white for main content */
            --bg-gray-50: #F9FAFB;                                    /* Light gray for secondary panels */
            --bg-gray-100: #F3F4F6;                                   /* Slightly darker for cards */
            --bg-gray-200: #E5E7EB;                                   /* Borders and dividers */
            
            /* Sidebar specific backgrounds (warm tint) */
            --sidebar-bg: {colors.get('sidebar', '#FFF9F0')};         /* Warm off-white with honey tint */
            --sidebar-hover: #FEF3E2;                                  /* Subtle gold tint on hover */
            --sidebar-active: #FEF7E8;                                 /* Cream background for active items */
            --sidebar-border: #F3E8D8;                                 /* Subtle gold-tinted border */
            
            /* Legacy backgrounds */
            --charcoal: #FFFFFF;                                       /* Inverted for light theme */
            --charcoal-light: #F9FAFB;                                 /* Light gray instead of dark */
            --creamy-white: {colors.get('background', '#FFFFFF')};
            --background: {colors.get('background', '#FFFFFF')};
            
            /* ==================== */
            /* Text Colors          */
            /* ==================== */
            --text-primary: {colors.get('text', '#111827')};          /* Almost black - body text (16:1) */
            --text-secondary: {colors.get('textSecondary', '#4B5563')}; /* Medium gray - labels (10:1) */
            --text-tertiary: #6B7280;                                  /* Light gray - metadata (7:1) */
            --text-disabled: #9CA3AF;                                  /* Very light gray - disabled (4.6:1) */
            --text-white: #FFFFFF;                                     /* For dark backgrounds */
            
            /* Text on colored backgrounds */
            --text-on-gold: #111827;                                   /* Dark text on gold buttons */
            --text-on-dark: #FFFFFF;                                   /* White text on dark elements */
            
            /* Legacy text colors */
            --dark-text: {colors.get('text', '#111827')};
            --medium-text: {colors.get('textSecondary', '#4B5563')};
            --text-gray-200: #E5E7EB;
            --text-gray-300: #D1D5DB;
            --text-gray-400: #9CA3AF;
            --text-gray-600: #4B5563;
            --text-gray-700: #374151;
            --text-gray-900: #111827;
            
            /* ==================== */
            /* Border Colors        */
            /* ==================== */
            --border-light: {colors.get('border', '#E5E7EB')};        /* Standard borders */
            --border-medium: #D1D5DB;                                  /* Slightly darker borders */
            --border-dark: #9CA3AF;                                    /* Prominent borders */
            --border-gold: {colors.get('secondary', '#DAA520')};      /* Gold borders for emphasis */
            --border-gold-light: rgba(218, 165, 32, 0.3);             /* Subtle gold tinted borders */
            
            /* ==================== */
            /* Shadow Colors        */
            /* ==================== */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            /* Gold shadow for emphasis */
            --shadow-gold: 0 0 20px rgba(218, 165, 32, 0.25);
            --shadow-gold-lg: 0 0 30px rgba(218, 165, 32, 0.3);
            
            /* ==================== */
            /* Interactive States   */
            /* ==================== */
            --hover-bg: #F9FAFB;                                       /* Generic hover background */
            --active-bg: #F3F4F6;                                      /* Generic active background */
            --focus-ring: {colors.get('secondary', '#DAA520')};       /* Gold focus ring */
            
            /* ==================== */
            /* Status Colors        */
            /* ==================== */
            --success: #059669;                                        /* Green for success */
            --success-bg: #D1FAE5;                                     /* Light green background */
            --warning: #D97706;                                        /* Orange for warnings */
            --warning-bg: #FEF3C7;                                     /* Light orange background */
            --error: #DC2626;                                          /* Red for errors */
            --error-bg: #FEE2E2;                                       /* Light red background */
            --info: #2563EB;                                           /* Blue for info */
            --info-bg: #DBEAFE;                                        /* Light blue background */
            
            /* ==================== */
            /* Effect Colors        */
            /* ==================== */
            --glow-gold: rgba(218, 165, 32, 0.3);                     /* Reduced for light theme */
            --glow-honey: rgba(255, 191, 0, 0.25);                    /* Reduced for light theme */
            --border-gold-20: rgba(218, 165, 32, 0.2);
            --border-gold-30: rgba(218, 165, 32, 0.3);
            --bg-gold-10: rgba(218, 165, 32, 0.1);
            --bg-honey-10: rgba(255, 191, 0, 0.1);
            
            /* Overlay colors */
            --overlay-light: rgba(255, 255, 255, 0.95);
            --overlay-dark: rgba(0, 0, 0, 0.5);
            
            /* ==================== */
            /* Additional Colors    */
            /* ==================== */
            --lavender: #C9A0DC;
            --soft-peach: #FFD8B1;
            --light-gray: #E8E8E8;
        }}
    """


def validate_branding_config(config_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate a branding configuration file.

    Args:
        config_path: Path to branding.json file

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not config_path.exists():
        return False, f"Configuration file not found: {config_path}"

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Check required field
        if "projectName" not in config:
            return False, "Missing required field: projectName"

        # Validate color format if provided
        if "colors" in config:
            colors = config["colors"]
            for color_key in ["primary", "secondary", "accent", "background"]:
                if color_key in colors:
                    color_value = colors[color_key]
                    if not isinstance(color_value, str) or not color_value.startswith('#'):
                        return False, f"Invalid color format for {color_key}: must be hex color (e.g., #A7C7E7)"

        return True, None

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"


def create_branding_file(output_path: Path, project_name: str, **kwargs) -> None:
    """
    Create a new branding configuration file.

    Args:
        output_path: Where to save branding.json
        project_name: Name of the project
        **kwargs: Additional branding options (shortName, welcomeMessage, colors, etc.)
    """
    branding = DEFAULT_BRANDING.copy()
    branding["projectName"] = project_name

    # Update with provided kwargs
    for key, value in kwargs.items():
        if key in branding:
            if isinstance(branding[key], dict) and isinstance(value, dict):
                branding[key].update(value)
            else:
                branding[key] = value

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(branding, f, indent=2)

    print(f"Created branding configuration: {output_path}")
