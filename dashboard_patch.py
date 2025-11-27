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

        # Patch the static file handler
        patch_static_handler(dashboard)

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


def patch_static_handler(dashboard_module):
    """
    Patch the DashboardRequestHandler to serve static files from .kittify/static.
    """
    import mimetypes
    import os
    
    # Get the handler class
    Handler = dashboard_module.DashboardRequestHandler
    original_do_GET = Handler.do_GET
    
    def custom_do_GET(self):
        """Custom GET handler that checks for project-specific static files first."""
        # Check if this is a static file request
        if self.path.startswith('/static/'):
            # Try to find the file in .kittify/static
            filename = self.path[len('/static/'):]
            
            # Look for .kittify directory
            current = Path.cwd()
            kittify_dir = None
            
            # First check if we are in the project root (common case)
            if (current / ".kittify").exists():
                kittify_dir = current / ".kittify"
            else:
                # Search up a few levels
                temp = current
                for _ in range(3):
                    if (temp / ".kittify").exists():
                        kittify_dir = temp / ".kittify"
                        break
                    temp = temp.parent
            
            if kittify_dir:
                custom_static_path = kittify_dir / "static" / filename
                if custom_static_path.exists() and custom_static_path.is_file():
                    try:
                        # Serve the custom file
                        mime_type, _ = mimetypes.guess_type(custom_static_path.name)
                        self.send_response(200)
                        self.send_header('Content-type', mime_type or 'application/octet-stream')
                        self.send_header('Cache-Control', 'no-cache')
                        self.end_headers()
                        
                        with open(custom_static_path, 'rb') as f:
                            self.wfile.write(f.read())
                        return
                    except Exception as e:
                        print(f"Error serving custom static file {filename}: {e}")
                        # Fall through to original handler on error
        
        # Fallback to original handler
        return original_do_GET(self)
    
    # Apply the patch
    Handler.do_GET = custom_do_GET
    print("✓ Static file handler patched for custom branding")

