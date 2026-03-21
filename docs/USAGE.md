# Usage Guide

## Basic Commands

### List Projects
```bash
/clawganizer "list projects"
```
Shows all active and archived projects.

### Create Project
```bash
/clawganizer "create project MyApp"
```
Creates new folder in `~/.openclaw/projects/active/MyApp`

### Archive Project
```bash
/clawganizer "archive MyApp"
```
Moves project from active to archived.

### Check Status
```bash
/clawganizer "status"
```
Shows workspace statistics.

### Organize Workspace
```bash
/clawganizer "organize"
```
Creates standard folder structure.

### Generate Documentation
```bash
/clawganizer "docs"
```
Auto-generates workspace documentation.

## Examples

### Scenario 1: New Development Environment
```bash
/clawganizer "organize"              # Set up workspace
/clawganizer "create project web"    # Create project
/clawganizer "create project api"    # Create another
/clawganizer "status"                # Check setup
```

### Scenario 2: Project Cleanup
```bash
/clawganizer "archive legacy"        # Archive old project
/clawganizer "archive deprecated"    # Archive another
/clawganizer "list projects"         # See updated list
```

### Scenario 3: Documentation
```bash
/clawganizer "docs"                  # Generate docs
```

## Tips

- Project names should be lowercase alphanumeric
- Use descriptive names for better organization
- Archive projects regularly to keep workspace clean
- Run `organize` once per machine to set up structure

