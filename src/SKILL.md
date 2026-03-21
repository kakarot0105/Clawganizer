---
name: clawganizer
description: "Clawganizer - OpenClaw Project Organizer. Organize, manage, and structure your OpenClaw workspace. Use /clawganizer to manage projects."
user-invocable: true
metadata: { "openclaw": { "emoji": "📁", "requires": {} } }
---

# Clawganizer - OpenClaw Project Organizer

Intelligent project organization and workspace management for OpenClaw.

## Features

- Create project structures
- Organize existing projects
- List and search projects
- Archive old projects
- Generate documentation
- Create folder hierarchies
- Project status tracking

## Usage

```bash
/clawganizer "create project MyProject"
/clawganizer "list projects"
/clawganizer "archive OldProject"
/clawganizer "organize workspace"
/clawganizer "generate docs"
```

## Commands

### Create Project
```
/clawganizer "create project {name} {description}"
```

### List Projects
```
/clawganizer "list projects"
/clawganizer "list all"
/clawganizer "status"
```

### Archive Project
```
/clawganizer "archive {project_name}"
```

### Organize Workspace
```
/clawganizer "organize"
/clawganizer "structure"
```

### Generate Documentation
```
/clawganizer "docs"
/clawganizer "generate readme"
```

## Configuration

Edit `config.json` to customize:
- Project folder structure
- Archive policy
- Documentation templates
- Naming conventions
