#!/bin/bash
# Safely start the dashboard for the current project
# Automatically finds an available port (9237, 9238, etc.)
# Does NOT overwrite project files (unlike 'spec-kitty init')

set -e

# Find python in spec-kitty venv
PIPX_VENV=$(find ~/.local/pipx/venvs -name "spec-kitty-cli" -type d 2>/dev/null | head -1)
if [ -z "$PIPX_VENV" ]; then
    echo "Error: spec-kitty-cli pipx environment not found."
    exit 1
fi

PYTHON_EXEC="$PIPX_VENV/bin/python"
if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC=$(find "$PIPX_VENV" -name "python" -type f | grep "/bin/python$" | head -1)
fi

if [ -z "$PYTHON_EXEC" ]; then
    PYTHON_EXEC="python3"
fi

echo "Starting dashboard using: $PYTHON_EXEC"

"$PYTHON_EXEC" -c "
import sys
import os
from pathlib import Path

try:
    from specify_cli.dashboard import start_dashboard
    
    cwd = Path.cwd()
    print(f'Starting dashboard for: {cwd.name}')
    
    # Start server (auto-finds port)
    port, _ = start_dashboard(cwd, background_process=True)
    
    dashboard_url = f'http://127.0.0.1:{port}'
    print(f'✅ Dashboard started at: {dashboard_url}')
    
    # Update .dashboard file so 'spec-kitty dashboard' command works
    kittify_dir = cwd / '.kittify'
    kittify_dir.mkdir(exist_ok=True)
    
    dashboard_file = kittify_dir / '.dashboard'
    dashboard_file.write_text(f'{dashboard_url}\n{port}\n', encoding='utf-8')
    print(f'   Updated {dashboard_file}')
    
    print(f'   Run \'spec-kitty dashboard\' to open it.')

except ImportError:
    print('Error: Could not import specify_cli. Is spec-kitty-cli installed?')
    sys.exit(1)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"
