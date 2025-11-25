#!/usr/bin/env python3
"""
Dashboard patch to add branding support to Spec Kitty.

This module monkey-patches the dashboard.py get_dashboard_html() function
to support customizable branding via .kittify/branding.json.
"""

import re
from pathlib import Path
from typing import Callable
from branding_loader import load_branding_config, get_css_variables


def patch_dashboard_html(original_func: Callable) -> Callable:
    """
    Wrap the original get_dashboard_html() to inject branding.

    Args:
        original_func: Original get_dashboard_html function

    Returns:
        Patched function that applies branding
    """
    def get_dashboard_html_branded() -> str:
        """Generate dashboard HTML with custom branding applied."""
        # Load branding configuration
        branding = load_branding_config()

        # Get original HTML
        html = original_func()

        # Apply branding replacements
        html = apply_branding(html, branding)

        return html

    return get_dashboard_html_branded


def apply_branding(html: str, branding: dict) -> str:
    """
    Apply branding configuration to dashboard HTML.

    Args:
        html: Original dashboard HTML
        branding: Branding configuration dictionary

    Returns:
        HTML with branding applied
    """
    # Replace page title
    html = html.replace(
        '<title>Spec Kitty Dashboard</title>',
        f'<title>{branding["projectName"]} Dashboard</title>'
    )

    # Replace favicon
    html = html.replace(
        'href="/static/spec-kitty.png">',
        f'href="{branding["faviconPath"]}">'
    )

    # Replace logo image src
    html = html.replace(
        'src="/static/spec-kitty.png" alt="Spec Kitty logo"',
        f'src="{branding["logoPath"]}" alt="{branding["projectName"]} logo"'
    )

    # Replace header title
    html = html.replace(
        '<h1>Spec Kitty</h1>',
        f'<h1>{branding["shortName"]}</h1>'
    )

    # Replace welcome message
    html = html.replace(
        '<h2>Welcome to Spec Kitty!</h2>',
        f'<h2>{branding["welcomeMessage"]}</h2>'
    )

    # Replace CSS color variables
    original_css_vars = """        :root {
            --baby-blue: #A7C7E7;
            --grassy-green: #7BB661;
            --lavender: #C9A0DC;
            --sunny-yellow: #FFF275;
            --soft-peach: #FFD8B1;
            --light-gray: #E8E8E8;
            --creamy-white: #FFFDF7;
            --dark-text: #2c3e50;
            --medium-text: #546e7a;
        }"""

    branded_css_vars = get_css_variables(branding)
    html = html.replace(original_css_vars, branded_css_vars)

    # Add footer if configured
    footer_config = branding.get("footer", {})
    if footer_config.get("text"):
        # Find the closing </body> tag and insert footer before it
        footer_html = create_footer_html(footer_config)
        html = html.replace('</body>', f'{footer_html}</body>')

    return html


def create_footer_html(footer_config: dict) -> str:
    """
    Create footer HTML from configuration.

    Args:
        footer_config: Footer configuration dict with 'text' and optional 'link'

    Returns:
        Footer HTML string
    """
    text = footer_config.get("text", "")
    link = footer_config.get("link", "")

    footer_style = """
    <style>
        .custom-footer {
            background: var(--creamy-white);
            padding: 20px;
            text-align: center;
            color: var(--medium-text);
            font-size: 0.9em;
            border-top: 2px solid var(--light-gray);
            margin-top: auto;
        }
        .custom-footer a {
            color: var(--grassy-green);
            text-decoration: none;
        }
        .custom-footer a:hover {
            text-decoration: underline;
        }
    </style>
    """

    if link:
        footer_content = f'<div class="custom-footer"><a href="{link}" target="_blank">{text}</a></div>'
    else:
        footer_content = f'<div class="custom-footer">{text}</div>'

    return footer_style + footer_content


def install_branding_patch():
    """
    Install the branding patch into the running dashboard module.

    This should be called early in the dashboard startup process.
    """
    try:
        # Import the dashboard module
        from specify_cli import dashboard

        # Get the original function
        original_get_dashboard_html = dashboard.get_dashboard_html

        # Create patched version
        patched_func = patch_dashboard_html(original_get_dashboard_html)

        # Replace the function in the module
        dashboard.get_dashboard_html = patched_func

        print("✓ Branding patch installed successfully")
        return True

    except ImportError as e:
        print(f"✗ Failed to import dashboard module: {e}")
        return False
    except AttributeError as e:
        print(f"✗ Dashboard module structure unexpected: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to install branding patch: {e}")
        return False
