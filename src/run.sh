#!/bin/bash
# Clawganizer - OpenClaw Project Organizer Skill

QUERY="$@"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw}"
PROJECTS_DIR="${WORKSPACE}/projects"

# Create directories if needed
mkdir -p "$PROJECTS_DIR"/{active,archived}

if [ -z "$QUERY" ]; then
    echo "📁 Clawganizer - OpenClaw Project Organizer"
    echo "Usage: /clawganizer <command>"
    echo ""
    echo "Commands:"
    echo "  create project <name>      - Create new project"
    echo "  list projects              - List all projects"
    echo "  organize                   - Organize workspace"
    echo "  archive <project>          - Archive a project"
    echo "  status                     - Workspace status"
    echo "  docs                       - Generate documentation"
    exit 0
fi

# Parse commands
case "$QUERY" in
    *"list"*)
        echo "📂 Projects in workspace:"
        echo ""
        echo "Active Projects:"
        if [ -d "$PROJECTS_DIR/active" ]; then
            ls -1 "$PROJECTS_DIR/active" | sed 's/^/  ✅ /'
        else
            echo "  (none)"
        fi
        echo ""
        echo "Archived Projects:"
        if [ -d "$PROJECTS_DIR/archived" ]; then
            ls -1 "$PROJECTS_DIR/archived" | sed 's/^/  📦 /'
        else
            echo "  (none)"
        fi
        ;;
        
    *"create"*)
        PROJECT_NAME=$(echo "$QUERY" | sed -E 's/.*create project ([^ ]+).*/\1/')
        if [ -z "$PROJECT_NAME" ] || [ "$PROJECT_NAME" = "$QUERY" ]; then
            echo "❌ Usage: create project <name>"
            exit 1
        fi
        
        mkdir -p "$PROJECTS_DIR/active/$PROJECT_NAME"
        echo "✅ Created project: $PROJECT_NAME"
        echo ""
        echo "Folder structure:"
        echo "  $PROJECTS_DIR/active/$PROJECT_NAME/"
        echo ""
        echo "Next steps:"
        echo "  1. cd $PROJECTS_DIR/active/$PROJECT_NAME"
        echo "  2. git init"
        echo "  3. Start coding!"
        ;;
        
    *"organize"*)
        echo "🔄 Organizing workspace..."
        mkdir -p "$PROJECTS_DIR"/{active,archived}
        mkdir -p "$WORKSPACE/venvs"
        mkdir -p "$WORKSPACE/workspace/{memory,skills,notes}"
        echo "✅ Workspace structure created"
        echo ""
        echo "Structure:"
        echo "  projects/"
        echo "    ├── active/"
        echo "    └── archived/"
        echo "  venvs/"
        echo "  workspace/"
        echo "    ├── memory/"
        echo "    ├── skills/"
        echo "    └── notes/"
        ;;
        
    *"archive"*)
        PROJECT_NAME=$(echo "$QUERY" | sed -E 's/.*archive ([^ ]+).*/\1/')
        if [ -z "$PROJECT_NAME" ] || [ "$PROJECT_NAME" = "$QUERY" ]; then
            echo "❌ Usage: archive <project_name>"
            exit 1
        fi
        
        if [ -d "$PROJECTS_DIR/active/$PROJECT_NAME" ]; then
            mv "$PROJECTS_DIR/active/$PROJECT_NAME" "$PROJECTS_DIR/archived/"
            echo "✅ Archived: $PROJECT_NAME"
        else
            echo "❌ Project not found: $PROJECT_NAME"
            exit 1
        fi
        ;;
        
    *"status"*)
        echo "📊 Workspace Status"
        echo ""
        ACTIVE_COUNT=$(ls -1 "$PROJECTS_DIR/active" 2>/dev/null | wc -l)
        ARCHIVED_COUNT=$(ls -1 "$PROJECTS_DIR/archived" 2>/dev/null | wc -l)
        echo "Active Projects: $ACTIVE_COUNT"
        echo "Archived Projects: $ARCHIVED_COUNT"
        echo "Workspace: $WORKSPACE"
        ;;
        
    *"docs"*)
        echo "📄 Generating documentation..."
        echo ""
        echo "# OpenClaw Workspace"
        echo ""
        echo "## Projects"
        echo ""
        if [ -d "$PROJECTS_DIR/active" ]; then
            ls -1 "$PROJECTS_DIR/active" | while read proj; do
                echo "### $proj"
                if [ -f "$PROJECTS_DIR/active/$proj/README.md" ]; then
                    echo "$(head -3 "$PROJECTS_DIR/active/$proj/README.md")"
                else
                    echo "*(No description)*"
                fi
                echo ""
            done
        fi
        ;;
        
    *)
        echo "❓ Unknown command: $QUERY"
        echo ""
        echo "Try: /clawganizer list projects"
        exit 1
        ;;
esac
