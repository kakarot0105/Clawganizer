#!/usr/bin/env bash
# Install Clawganizer globally for the current user.
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pip install --user .
BIN_DIR="$(python3 -m site --user-base)/bin"

echo ""
echo "Installed. Ensure this is on your PATH:"
echo "  export PATH=\"$BIN_DIR:\$PATH\""
echo ""
echo "Then:"
echo "  clawganizer status"
echo "  clawganizer run            # dry-run preview"
echo "  clawganizer run --apply    # organize your computer"
