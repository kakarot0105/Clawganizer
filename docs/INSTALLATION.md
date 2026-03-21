# Installation Guide

## Requirements

- OpenClaw (any version)
- Bash shell
- ~2MB disk space

## Installation Methods

### Method 1: Copy to Skills Directory (Recommended)

```bash
# Clone or download the repository
git clone https://github.com/kakarot0105/Clawganizer.git

# Copy to OpenClaw skills
cp -r Clawganizer ~/.openclaw/skills/clawganizer

# Verify installation
ls ~/.openclaw/skills/clawganizer
```

### Method 2: From GitHub

```bash
# Navigate to skills directory
cd ~/.openclaw/skills

# Clone directly
git clone https://github.com/kakarot0105/Clawganizer.git clawganizer

# Done!
```

### Method 3: Manual Download

1. Download ZIP from GitHub
2. Extract to `~/.openclaw/skills/clawganizer/`
3. Make run.sh executable: `chmod +x ~/.openclaw/skills/clawganizer/run.sh`

## Verify Installation

```bash
# Test the skill
bash ~/.openclaw/skills/clawganizer/run.sh "status"

# Expected output: Workspace Status
```

## Troubleshooting

### "Command not found"
- Verify OpenClaw is installed: `which openclaw`
- Check skills directory exists: `ls ~/.openclaw/skills`

### "Permission denied"
- Make run.sh executable: `chmod +x ~/.openclaw/skills/clawganizer/run.sh`

### "Workspace not found"
- Run: `/clawganizer "organize"` to create structure

## Next Steps

- Read [USAGE.md](USAGE.md) for command reference
- Check [CONFIG.md](CONFIG.md) for customization

