#!/bin/bash
# Artifact Shield Installation Script
# Self-configuring and fail-proof

set +e  # Don't exit on errors (fail-safe)

echo "🛡️  Installing Artifact Virtual Shield256..."
echo ""

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "❌ Not a git repository"
    exit 1
fi

# Paths
SHIELD_SCRIPTS="$REPO_ROOT/scripts/shield"
GIT_HOOKS="$REPO_ROOT/.git/hooks"

echo "📁 Repository: $REPO_ROOT"
echo "📁 Shield scripts: $SHIELD_SCRIPTS"
echo "📁 Git hooks: $GIT_HOOKS"
echo ""

# Make shield scripts executable
echo "🔧 Making shield scripts executable..."
chmod +x "$SHIELD_SCRIPTS/shield256.py" 2>/dev/null || echo "⚠️  Warning: Could not chmod shield256.py"
chmod +x "$SHIELD_SCRIPTS/pre_commit_hook.py" 2>/dev/null || echo "⚠️  Warning: Could not chmod pre_commit_hook.py"
chmod +x "$SHIELD_SCRIPTS/pre_push_hook.py" 2>/dev/null || echo "⚠️  Warning: Could not chmod pre_push_hook.py"

# Install pre-commit hook
echo "🪝 Installing pre-commit hook..."
cat > "$GIT_HOOKS/pre-commit" << 'EOF'
#!/bin/bash
# Artifact Shield Pre-Commit Hook
# Auto-encrypts sensitive files before commit

REPO_ROOT=$(git rev-parse --show-toplevel)
python3 "$REPO_ROOT/scripts/shield/pre_commit_hook.py"
HOOK_EXIT=$?
if [ $HOOK_EXIT -ne 0 ]; then
  echo "❌ Shield pre-commit check failed (exit $HOOK_EXIT). Commit blocked."
  echo "   Fix the issues above or use --no-verify to bypass."
fi
exit $HOOK_EXIT
EOF

chmod +x "$GIT_HOOKS/pre-commit" 2>/dev/null || echo "⚠️  Warning: Could not chmod pre-commit hook"

# Install pre-push hook
echo "🪝 Installing pre-push hook..."
cat > "$GIT_HOOKS/pre-push" << 'EOF'
#!/bin/bash
# Artifact Shield Pre-Push Hook
# Auto-purges old git history before push

REPO_ROOT=$(git rev-parse --show-toplevel)
python3 "$REPO_ROOT/scripts/shield/pre_push_hook.py"
HOOK_EXIT=$?
if [ $HOOK_EXIT -ne 0 ]; then
  echo "❌ Shield pre-push check failed (exit $HOOK_EXIT). Push blocked."
  echo "   Fix the issues above or use --no-verify to bypass."
fi
exit $HOOK_EXIT
EOF

chmod +x "$GIT_HOOKS/pre-push" 2>/dev/null || echo "⚠️  Warning: Could not chmod pre-push hook"

# Create alias for easy access
echo "🔗 Creating command alias..."

# Check if alias already exists
if ! grep -q "alias shield=" "$HOME/.bashrc" 2>/dev/null; then
    cat >> "$HOME/.bashrc" << EOF

# Artifact Shield Alias
alias shield='python3 $SHIELD_SCRIPTS/shield256.py'
EOF
    echo "✅ Added 'shield' alias to ~/.bashrc"
else
    echo "ℹ️  'shield' alias already exists in ~/.bashrc"
fi

# Also create a symlink if possible
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    ln -sf "$SHIELD_SCRIPTS/shield256.py" "/usr/local/bin/shield" 2>/dev/null
    echo "✅ Created system-wide 'shield' command"
else
    echo "ℹ️  Run 'source ~/.bashrc' to use 'shield' command"
fi

# Update .gitignore
echo "📝 Updating .gitignore..."
GITIGNORE="$REPO_ROOT/.gitignore"

if [ -f "$GITIGNORE" ]; then
    # Add shield entries if not already present
    if ! grep -q ".artifact_shield" "$GITIGNORE" 2>/dev/null; then
        echo "" >> "$GITIGNORE"
        echo "# Artifact Shield - Encryption keys and config" >> "$GITIGNORE"
        echo ".artifact_shield/" >> "$GITIGNORE"
        echo "*.enc.backup" >> "$GITIGNORE"
    fi
fi

# Create initial configuration
echo "⚙️  Creating initial configuration..."
python3 "$SHIELD_SCRIPTS/shield256.py" status . >/dev/null 2>&1 || true

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ Artifact Shield Installed Successfully!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📚 Quick Start:"
echo "   shield                    # Run interactive mode"
echo "   shield encrypt file.md    # Encrypt a file"
echo "   shield decrypt file.md.enc  # Decrypt a file"
echo "   shield status            # Check encryption status"
echo ""
echo "🔐 Features Enabled:"
echo "   ✓ Pre-commit encryption check (auto-encrypts sensitive files)"
echo "   ✓ Pre-push history purge (keeps last 5 commits)"
echo "   ✓ Hooks block on failure (bypass with git --no-verify)"
echo "   ✓ Audit logging to ~/.artifact_shield/audit.log"
echo ""
echo "⚙️  Configuration:"
echo "   Config: ~/.artifact_shield/config.json"
echo "   Keys: ~/.artifact_shield/keystore.dat"
echo "   Logs: ~/.artifact_shield/audit.log"
echo ""
echo "💡 Tips:"
echo "   - Set SHIELD_PASSPHRASE env var to avoid prompts"
echo "   - Set SHIELD_PURGE_DISABLED=1 to temporarily disable purge"
echo "   - Classification markers: TOP_SECRET, CONFIDENTIAL, RESTRICTED"
echo ""
echo "🔒 Security Note:"
echo "   Never commit your passphrase or keys to the repository!"
echo "   The .gitignore has been updated to protect ~/.artifact_shield/"
echo ""
echo "═══════════════════════════════════════════════════════"
