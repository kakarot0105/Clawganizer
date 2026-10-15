#!/usr/bin/env bash
# Clawganizer OpenClaw skill bridge → prefers the global Python CLI.
set -euo pipefail

QUERY="${*:-}"

if command -v clawganizer >/dev/null 2>&1; then
  if [[ -z "$QUERY" ]]; then
    exec clawganizer status
  fi
  case "$QUERY" in
    *organize*|*structure*)
      # Whole-computer organize when installed globally
      exec clawganizer run
      ;;
    *list*|*status*)
      if [[ "$QUERY" == *workspace* ]] || [[ "$QUERY" == *project* ]]; then
        exec clawganizer workspace list
      fi
      exec clawganizer status
      ;;
    *create*)
      NAME=$(echo "$QUERY" | sed -E 's/.*create project[[:space:]]+([^[:space:]]+).*/\1/')
      exec clawganizer workspace create "$NAME"
      ;;
    *archive*)
      NAME=$(echo "$QUERY" | sed -E 's/.*archive[[:space:]]+([^[:space:]]+).*/\1/')
      exec clawganizer workspace archive "$NAME"
      ;;
    *docs*)
      exec clawganizer workspace status
      ;;
    *)
      echo "Forwarding to: clawganizer run"
      exec clawganizer run
      ;;
  esac
fi

# Fallback: legacy OpenClaw-only bash helper (no global install)
WORKSPACE="${WORKSPACE:-$HOME/.openclaw}"
PROJECTS_DIR="${WORKSPACE}/projects"
mkdir -p "$PROJECTS_DIR"/{active,archived}

if [[ -z "$QUERY" ]]; then
  echo "Clawganizer (skill fallback)"
  echo "Install globally for whole-computer organize:"
  echo "  pip install git+https://github.com/kakarot0105/Clawganizer.git"
  echo "  clawganizer run --apply"
  exit 0
fi

case "$QUERY" in
  *"list"*)
    echo "Active:"; ls -1 "$PROJECTS_DIR/active" 2>/dev/null || true
    echo "Archived:"; ls -1 "$PROJECTS_DIR/archived" 2>/dev/null || true
    ;;
  *"create"*)
    PROJECT_NAME=$(echo "$QUERY" | sed -E 's/.*create project ([^ ]+).*/\1/')
    mkdir -p "$PROJECTS_DIR/active/$PROJECT_NAME"
    echo "Created: $PROJECT_NAME"
    ;;
  *"organize"*)
    mkdir -p "$PROJECTS_DIR"/{active,archived}
    mkdir -p "$WORKSPACE/venvs"
    mkdir -p "$WORKSPACE/workspace"/{memory,skills,notes}
    echo "OpenClaw workspace structure created (install CLI for whole-computer organize)"
    ;;
  *"archive"*)
    PROJECT_NAME=$(echo "$QUERY" | sed -E 's/.*archive ([^ ]+).*/\1/')
    mv "$PROJECTS_DIR/active/$PROJECT_NAME" "$PROJECTS_DIR/archived/"
    echo "Archived: $PROJECT_NAME"
    ;;
  *"status"*)
    echo "Active: $(ls -1 "$PROJECTS_DIR/active" 2>/dev/null | wc -l)"
    echo "Archived: $(ls -1 "$PROJECTS_DIR/archived" 2>/dev/null | wc -l)"
    ;;
  *)
    echo "Unknown command: $QUERY"
    exit 1
    ;;
esac
