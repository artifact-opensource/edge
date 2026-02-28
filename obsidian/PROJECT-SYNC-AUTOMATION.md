# ↻ PROJECT SYNC AUTOMATION REMINDER

## ! ACTION REQUIRED: Set Up Automated Project Repository Synchronization

**Priority:** High  
**Deadline:** Before next major project updates  
**Status:** 🔴 Not Started

---

## 📋 Overview

Create automated synchronization between external project repositories and local `enterprise/projects/` directories to keep documentation automatically updated without manual intervention.

**Current State:**
- 17 project directories in `enterprise/projects/` with comprehensive documentation
- Each project has external GitHub repository (Artifact-Virtual org or amuzetnoM)
- Documentation must be manually updated when projects change

**Goal:**
- Automatic sync from external repos → local project directories
- Automatic commit and push to enterprise repo
- Minimal manual intervention
- Real-time or scheduled updates

---

## ◉ RECOMMENDED SOLUTION: GitHub Actions Workflow

### Why This Approach?

✓ **Pros:**
- Native GitHub integration (no external services)
- Scheduled or event-triggered updates
- Full control over sync logic
- Free for public/private repos
- Audit trail in Actions logs
- Can run on multiple repositories simultaneously

❌ **Alternative Rejected:**
- Git submodules: Too complex, requires manual updates
- Webhooks + external server: Requires infrastructure, costs money
- Manual scripts: Not truly automated, prone to errors

### Implementation Strategy

Use **GitHub Actions** with **repository dispatch events** and **scheduled workflows**:

1. **External repos** → Trigger webhook on push/release
2. **Enterprise repo** → Receives webhook, pulls updates, commits changes
3. **Scheduled fallback** → Daily/weekly sync to catch any missed updates

---

## 🛠️ IMPLEMENTATION INSTRUCTIONS

### Phase 1: Set Up GitHub Actions Workflow (Enterprise Repo)

**File:** `.github/workflows/sync-project-docs.yml`

```yaml
name: Sync Project Documentation

on:
  # Trigger on external repository updates
  repository_dispatch:
    types: [project-updated]
  
  # Scheduled daily sync at 2 AM UTC
  schedule:
    - cron: '0 2 * * *'
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      project:
        description: 'Specific project to sync (or "all")'
        required: false
        default: 'all'

jobs:
  sync-projects:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout enterprise repo
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0
      
      - name: Set up Git
        run: |
          git config user.name "Project Sync Bot"
          git config user.email "bot@artifact-virtual.com"
      
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y jq
      
      - name: Sync project documentation
        env:
          GH_TOKEN: ${{ secrets.PAT_TOKEN }}
        run: |
          chmod +x scripts/sync-project-docs.sh
          ./scripts/sync-project-docs.sh
      
      - name: Commit and push changes
        run: |
          git add enterprise/projects/
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "chore: Auto-sync project documentation from external repos [skip ci]"
            git push origin main
          fi
```

---

### Phase 2: Create Sync Script

**File:** `scripts/sync-project-docs.sh`

```bash
#!/bin/bash
set -e

TEMP_DIR="/tmp/project-sync"
PROJECTS_DIR="enterprise/projects"

# Project mapping: directory name → GitHub repo URL
declare -A PROJECTS=(
  ["arc"]="https://github.com/Artifact-Virtual/ARC.git"
  ["reason"]="https://github.com/Artifact-Virtual/REASON.git"
  ["sentinel"]="https://github.com/Artifact-Virtual/SENTINEL.git"
  ["outcome"]="https://github.com/Artifact-Virtual/PROJECT-OUTCOME.git"
  ["avpm"]="https://github.com/amuzetnoM/gh_projects.git"
  ["artifact-erp"]="https://github.com/amuzetnoM/business_erp.git"
  ["cthulu"]="https://github.com/amuzetnoM/cthulu.git"
  ["sdk"]="https://github.com/amuzetnoM/ARTIFACT-SDK.git"
  ["gladius"]="https://github.com/Artifact-Virtual/GLADIUS.git"
  ["syndicate"]="https://github.com/amuzetnoM/syndicate.git"
  ["hektor"]="https://github.com/amuzetnoM/hektor.git"
  ["virtual-lab"]="https://github.com/amuzetnoM/artifact_lab.git"
  ["research"]="https://github.com/amuzetnoM/research.git"
  ["ava"]="https://github.com/amuzetnoM/AVA.git"
  ["meteor"]="https://github.com/amuzetnoM/project_manager.git"
  ["dockit"]="https://github.com/amuzetnoM/dockit-app.git"
  ["orxl"]="https://github.com/amuzetnoM/orxl.git"
)

# Files to sync from external repo to enterprise
FILES_TO_SYNC=(
  "README.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "docs/ARCHITECTURE.md:ARCHITECTURE.md"
)

mkdir -p "$TEMP_DIR"

sync_project() {
  local project=$1
  local repo_url=$2
  
  echo "↻ Syncing $project from $repo_url"
  
  # Clone external repo
  local clone_dir="$TEMP_DIR/$project"
  rm -rf "$clone_dir"
  git clone --depth 1 "$repo_url" "$clone_dir" 2>/dev/null || {
    echo "!  Failed to clone $project, skipping..."
    return
  }
  
  # Sync each file
  for file_map in "${FILES_TO_SYNC[@]}"; do
    IFS=':' read -r src_file dest_file <<< "$file_map"
    dest_file=${dest_file:-$src_file}
    
    src_path="$clone_dir/$src_file"
    dest_path="$PROJECTS_DIR/$project/$dest_file"
    
    if [ -f "$src_path" ]; then
      echo "  ✓ Syncing $src_file → $dest_file"
      cp "$src_path" "$dest_path"
      
      # Add sync timestamp
      echo "" >> "$dest_path"
      echo "---" >> "$dest_path"
      echo "*Last synced: $(date -u '+%Y-%m-%d %H:%M:%S UTC') from external repo ($repo_url)*" >> "$dest_path"
    fi
  done
  
  # Update STATUS.md with latest commit info
  local latest_commit=$(cd "$clone_dir" && git log -1 --format="%h - %s (%ar)" 2>/dev/null || echo "Unknown")
  local status_file="$PROJECTS_DIR/$project/STATUS.md"
  
  if [ -f "$status_file" ]; then
    # Update "Latest External Commit" section if it exists
    sed -i "/Latest External Commit:/c\\**Latest External Commit:** $latest_commit" "$status_file" || true
  fi
  
  echo "  ✓ Completed $project"
}

# Sync all projects
for project in "${!PROJECTS[@]}"; do
  sync_project "$project" "${PROJECTS[$project]}"
done

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ All projects synced successfully!"
```

**Make executable:**
```bash
chmod +x scripts/sync-project-docs.sh
```

---

### Phase 3: Set Up Repository Dispatch (Optional - For Real-Time Updates)

**In each external project repo** (e.g., HEKTOR, CTHULU, etc.), add webhook workflow:

**File:** `.github/workflows/notify-enterprise.yml`

```yaml
name: Notify Enterprise on Update

on:
  push:
    branches: [main, master]
  release:
    types: [published]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger enterprise sync
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Authorization: token ${{ secrets.ENTERPRISE_DISPATCH_TOKEN }}" \
            https://api.github.com/repos/amuzetnoM/enterprise/dispatches \
            -d '{"event_type":"project-updated","client_payload":{"project":"${{ github.event.repository.name }}"}}'
```

**Required:** Create `ENTERPRISE_DISPATCH_TOKEN` secret in each external repo with PAT that has `repo` scope.

---

### Phase 4: Security Configuration

**Create Personal Access Token (PAT):**

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes:
   - ✓ `repo` (full control of private repositories)
   - ✓ `workflow` (update GitHub Actions workflows)
3. Name it: `Enterprise Project Sync Token`
4. Set expiration: 1 year (set calendar reminder to renew)
5. Save token securely

**Add to Enterprise Repo:**
1. Go to enterprise repo → Settings → Secrets and variables → Actions
2. Create new secret: `PAT_TOKEN`
3. Paste the PAT token

---

## ■ SYNC BEHAVIOR CONFIGURATION

### What Gets Synced

**FROM external repos:**
- ✓ README.md (project overview)
- ✓ CHANGELOG.md (version history)
- ✓ CONTRIBUTING.md (development guidelines)
- ✓ docs/ARCHITECTURE.md (technical docs)

**STAYS LOCAL in enterprise repo:**
- ✓ STATUS.md (enterprise-specific status tracking)
- ✓ ROADMAP.md (enterprise strategic planning)
- ✓ Local annotations and enterprise context

### Sync Frequency

- **Real-time:** When external repo pushes to main/master (via repository_dispatch)
- **Scheduled:** Daily at 2 AM UTC (fallback for missed events)
- **Manual:** Via GitHub Actions UI when needed

### Conflict Resolution

- External repo content **overwrites** local synced files
- Local-only files (STATUS.md, ROADMAP.md) are **never** overwritten
- Sync timestamp appended to synced files for audit trail

---

## 🔐 ALTERNATIVE: Git Submodules (Not Recommended)

If you prefer submodules (not recommended due to complexity):

```bash
# Add each project as submodule
git submodule add https://github.com/Artifact-Virtual/ARC.git enterprise/projects/arc/external
git submodule add https://github.com/amuzetnoM/hektor.git enterprise/projects/hektor/external

# Update all submodules
git submodule update --remote --merge

# Commit submodule updates
git add .gitmodules enterprise/projects/*/external
git commit -m "Update project submodules"
```

**Why NOT recommended:**
- Manual `git submodule update` required
- Nested .git directories complicate structure
- Merge conflicts more common
- Harder to customize what gets synced

---

## → GETTING STARTED CHECKLIST

### Immediate Actions:

- [ ] **Step 1:** Create PAT token with `repo` + `workflow` scopes
- [ ] **Step 2:** Add `PAT_TOKEN` secret to enterprise repo
- [ ] **Step 3:** Create `.github/workflows/sync-project-docs.yml` in enterprise repo
- [ ] **Step 4:** Create `scripts/sync-project-docs.sh` in enterprise repo
- [ ] **Step 5:** Test workflow manually via GitHub Actions UI
- [ ] **Step 6:** Verify sync in `enterprise/projects/` directories
- [ ] **Step 7:** (Optional) Add webhook workflows to high-priority external repos

### Ongoing Maintenance:

- [ ] **Monthly:** Review Actions logs for failed syncs
- [ ] **Quarterly:** Update project mappings if repos change
- [ ] **Annually:** Renew PAT token before expiration
- [ ] **As needed:** Adjust sync frequency in workflow schedule

---

## 📝 TESTING INSTRUCTIONS

### Manual Test Run:

1. Go to enterprise repo on GitHub
2. Navigate to **Actions** tab
3. Select **Sync Project Documentation** workflow
4. Click **Run workflow** dropdown
5. Select branch: `main`
6. Input: `all` (or specific project like `hektor`)
7. Click **Run workflow**
8. Monitor logs for success/failures
9. Check `enterprise/projects/` for updated files

### Verify Sync:

```bash
# Check sync timestamps
grep "Last synced:" enterprise/projects/*/README.md

# Check for recent updates
git log --oneline --all --grep="Auto-sync" -10
```

---

## 🐛 TROUBLESHOOTING

### Issue: Workflow not triggering

**Solution:**
- Verify PAT token has correct scopes
- Check token hasn't expired
- Ensure workflow file syntax is valid (use YAML validator)

### Issue: Clone failures

**Solution:**
- Verify repo URLs are correct in script
- Check if repos are private (PAT needs access)
- Ensure network connectivity in Actions runner

### Issue: Permission denied

**Solution:**
- Verify PAT token is added as `PAT_TOKEN` secret
- Ensure PAT has `repo` scope for all target repositories
- Check token hasn't been revoked

### Issue: No changes detected

**Solution:**
- External repos may not have changed
- Check if sync is pulling from correct branch
- Verify FILES_TO_SYNC array includes desired files

---

## 💡 ADVANCED FEATURES (Future Enhancements)

### Selective Syncing

Modify script to sync only specific projects:

```bash
# Sync only AI/ML projects
SYNC_FILTER="hektor cthulu gladius reason sentinel orxl"
```

### Change Detection Notifications

Add Slack/Discord webhook to notify on sync:

```yaml
- name: Notify on sync
  if: success()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"✓ Project docs synced successfully"}'
```

### Smart Merging

Instead of overwriting, use `git diff` to preserve local edits:

```bash
# Merge instead of overwrite
git merge --no-commit --no-ff external/main
git checkout --ours STATUS.md ROADMAP.md
```

---

## ▫ DOCUMENTATION LINKS

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Repository Dispatch Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch)
- [Creating Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/bash.html)

---

## ✓ COMPLETION CRITERIA

This task is complete when:

1. ✓ GitHub Actions workflow is running successfully
2. ✓ Daily syncs execute without errors
3. ✓ Project documentation stays updated automatically
4. ✓ No manual intervention required for routine syncs
5. ✓ Sync timestamps visible in synced files
6. ✓ Enterprise-specific files (STATUS.md, ROADMAP.md) remain untouched

---

**Reminder set:** ▪ Review this document before next major project update cycle

**Priority:** 🔴 High - Implement within next sprint

**Estimated effort:** 2-4 hours for initial setup + testing

---

*Created: February 6, 2026*  
*Location: `.obsidian-reminders/PROJECT-SYNC-AUTOMATION.md`*  
*Status: 🔴 Action Required*
