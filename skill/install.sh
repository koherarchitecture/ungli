#!/usr/bin/env bash
# Installs the ungli skill for Claude Code and starts a fresh session with it loaded.
# Run from anywhere: bash install.sh
set -euo pipefail
src=$(cd "$(dirname "$0")" && pwd)
dest="$HOME/.claude/skills/ungli"

command -v claude >/dev/null || { echo "Claude Code is not installed (no 'claude' command). Install it first: https://code.claude.com/docs"; exit 1; }

mkdir -p "$HOME/.claude/skills"
rm -rf "$dest"
cp -R "$src" "$dest"
rm -f "$dest/install.sh"
echo "Installed to $dest"

# Skills load when a session starts, so a session already open will not see this one.
if pgrep -x claude >/dev/null; then
  echo "A Claude Code session is already open. Close it (type /exit there), then press Enter here."
  read -r _
fi
echo "Starting Claude Code with the skill loaded..."
exec claude "/ungli"
