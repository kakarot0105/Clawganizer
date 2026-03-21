# Clawganizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)

An intelligent OpenClaw skill for managing and organizing your development workspace.

## 📋 Features

- ✅ **Create Projects** - Generate new project folders with proper structure
- ✅ **List Projects** - View all active and archived projects
- ✅ **Archive Projects** - Move old projects to archive
- ✅ **Auto-Organize** - Generate workspace folder hierarchy
- ✅ **Status Tracking** - Monitor workspace statistics
- ✅ **Documentation** - Auto-generate workspace docs

## 🚀 Quick Start

### Installation

#### Option 1: Copy to OpenClaw Skills
```bash
mkdir -p ~/.openclaw/skills
cp -r . ~/.openclaw/skills/clawganizer/
```

#### Option 2: From GitHub
```bash
git clone https://github.com/kakarot0105/Clawganizer.git
cp -r Clawganizer ~/.openclaw/skills/clawganizer/
```

### Usage

In OpenClaw/Telegram:

```bash
# List all projects
/clawganizer "list projects"

# Create new project
/clawganizer "create project MyApp"

# Check workspace status
/clawganizer "status"

# Archive old project
/clawganizer "archive OldProject"

# Auto-organize workspace
/clawganizer "organize"

# Generate documentation
/clawganizer "docs"
```

## 📁 Workspace Structure

After running `organize`, your workspace looks like:

```
~/.openclaw/
├── projects/
│   ├── active/
│   │   ├── Project1/
│   │   └── Project2/
│   └── archived/
│       └── OldProject/
├── venvs/
├── workspace/
│   ├── memory/
│   ├── skills/
│   └── notes/
└── .openclaw.yaml
```

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [Configuration](docs/CONFIG.md)
- [Contributing](CONTRIBUTING.md)

## 🛠️ Commands Reference

### Create Project
```bash
/clawganizer "create project {name} {optional-description}"
```

### List Projects
```bash
/clawganizer "list projects"
/clawganizer "list all"
```

### Archive
```bash
/clawganizer "archive {project_name}"
```

### Organize
```bash
/clawganizer "organize"
```

### Status
```bash
/clawganizer "status"
```

### Generate Docs
```bash
/clawganizer "docs"
```

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Development

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

**Kakarot0105**

## 🙏 Acknowledgments

- Built for [OpenClaw](https://github.com/openclaw/openclaw)
- Inspired by modern DevOps tooling

---

**Status:** Production Ready ✅  
**Latest Version:** 1.0.0  
**Last Updated:** 2026-03-20

