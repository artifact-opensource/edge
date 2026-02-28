# Scripts Directory

This directory contains utility scripts and tools for the Artifact Virtual Business Infrastructure.

## Available Tools

### 📄 Copyright Tool
**Purpose**: Manage copyright information, front matter, and meta banners for all markdown files.

**Files**:
- `copyright-tool.js` - Main tool (Node.js)
- `run-copyright-tool.sh` - Wrapper script (Bash)
- `run-copyright-tool.ps1` - Wrapper script (PowerShell)
- `test-copyright-tool.js` - Comprehensive test suite
- `COPYRIGHT_TOOL_README.md` - Full documentation
- `COPYRIGHT_TOOL_EXAMPLES.md` - Before/after examples

**Quick Start**:
```bash
# Interactive menu (recommended)
./run-copyright-tool.sh

# Or run directly
node copyright-tool.js --dry-run    # Preview changes
node copyright-tool.js              # Apply to current directory
node copyright-tool.js --path .     # Apply to entire repo
```

**Key Features**:
- ✓ Adds consistent front matter to all markdown files
- ✓ Injects non-rendering Artifact Virtual banner
- ✓ Smart merging with existing metadata
- ✓ Backup mechanism for safety
- ✓ Dry-run mode for preview
- ✓ Idempotent (safe to run multiple times)

**Documentation**: See COPYRIGHT_TOOL_README.md (planned)

---

### 📡 Fetch Scripts
**Purpose**: Fetch and synchronize data from external sources.

**Files**:
- `fetch.sh` - Bash fetch script
- `fetch.ps1` - PowerShell fetch script

---

### ↻ Notion Integration
**Purpose**: Integration tools for Notion workspace.

**Directory**: `notion/`

---

## Usage Guidelines

### Running Scripts

#### Bash (Linux/macOS)
```bash
# Make script executable (if needed)
chmod +x script-name.sh

# Run script
./script-name.sh
```

#### PowerShell (Windows)
```powershell
# Run script
.\script-name.ps1
```

#### Node.js
```bash
# Run Node.js script
node script-name.js [options]
```

### Best Practices

1. **Always test with dry-run first** when available
2. **Review changes** before committing
3. **Keep backups** enabled (default for copyright tool)
4. **Read documentation** before using unfamiliar tools
5. **Report issues** if you encounter problems

## Copyright Tool - Detailed Usage

### Common Commands

```bash
# Preview what would change
node copyright-tool.js --dry-run

# Process current directory
node copyright-tool.js

# Process specific directory
node copyright-tool.js --path ../docs

# Process with verbose output
node copyright-tool.js --verbose

# Process without creating backups (not recommended)
node copyright-tool.js --no-backup

# Show help
node copyright-tool.js --help

# Run test suite
node test-copyright-tool.js
```

### Interactive Wrapper

The wrapper scripts (`run-copyright-tool.sh` and `run-copyright-tool.ps1`) provide an interactive menu:

```bash
./run-copyright-tool.sh
```

Menu options:
1. Preview changes (dry-run) on current directory
2. Apply to current directory
3. Apply to entire repository
4. Show help
5. Run tests

### Examples

See COPYRIGHT_TOOL_EXAMPLES.md (planned) for detailed before/after examples.

## Testing

### Copyright Tool Tests

Run the comprehensive test suite:
```bash
node test-copyright-tool.js
```

Test coverage includes:
- File discovery (nested directories)
- Banner injection (HTML comment format)
- Front matter addition
- Front matter preservation and merging
- Idempotency
- Backup creation
- Dry-run mode
- No-backup mode
- Ignore patterns
- Title generation
- Deep nesting
- HTML comment format validation

**Current Status**: 38/38 tests passing (100%)

## Requirements

### Copyright Tool
- **Node.js**: v12 or higher (uses built-in modules only)
- **No external dependencies**

### Fetch Scripts
- Bash or PowerShell depending on platform

### Notion Tools
- Python 3.x (see `notion/` directory for details)

## Troubleshooting

### Copyright Tool

**Problem**: "No files found"
- **Solution**: Check you're in the correct directory or use `--path` option

**Problem**: Permission errors
- **Solution**: Ensure you have write permissions: `ls -la`

**Problem**: Tool not running
- **Solution**: Check Node.js is installed: `node --version`

### General

**Problem**: Script not executable
- **Solution**: `chmod +x script-name.sh`

**Problem**: PowerShell execution policy
- **Solution**: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Maintenance

### Updating Scripts
1. Test changes in isolated environment first
2. Run test suites if available
3. Update documentation
4. Update version numbers if applicable

### Adding New Scripts
1. Place in appropriate location
2. Add documentation to this README
3. Make executable if shell script
4. Follow existing naming conventions
5. Include usage examples

## Security Considerations

### Copyright Tool
- Creates backups by default (`.backup-*` files)
- Reads organization info from `artifact-project.json`
- Marks documents as confidential by default
- Tracks file modifications with timestamps

### General
- Review scripts before running
- Use dry-run when available
- Check file permissions
- Don't commit sensitive data

## Support

For issues or questions:
1. Check documentation in this directory
2. Run with `--help` or `--verbose` flags
3. Review error messages carefully
4. Check file permissions and Node.js installation

## File Organization

```
scripts/
├── README.md (this file)
├── copyright-tool.js              # Main copyright tool
├── run-copyright-tool.sh          # Bash wrapper
├── run-copyright-tool.ps1         # PowerShell wrapper
├── test-copyright-tool.js         # Test suite
├── COPYRIGHT_TOOL_README.md       # Detailed documentation
├── COPYRIGHT_TOOL_EXAMPLES.md     # Examples
├── fetch.sh                       # Fetch script (Bash)
├── fetch.ps1                      # Fetch script (PowerShell)
└── notion/                        # Notion integration tools
```

## License

All scripts are part of the Artifact Virtual Business Infrastructure.

© 2026 Artifact Virtual (SMC-Private) Limited. All rights reserved.
