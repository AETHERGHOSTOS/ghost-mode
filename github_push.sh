#!/bin/bash
# ============================================================
# 💀 AETHER GHOST OS — GitHub Repository Setup Script
# Run this ONCE to push your project to GitHub
# ============================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "  ${CYAN}→  $1${NC}"; }
err()  { echo -e "  ${RED}❌ $1${NC}"; }

echo ""
echo -e "  ${CYAN}💀 AETHER GHOST OS — GitHub Setup Script${NC}"
echo "  ============================================="
echo ""

# ─── STEP 1: CHECK GIT ────────────────────────────────────
if ! command -v git &>/dev/null; then
  err "Git is not installed."
  info "Install with: pkg install git (Termux) | apt install git (Linux) | brew install git (macOS)"
  exit 1
fi
ok "Git is installed"

# ─── STEP 2: CONFIGURE GIT USER ───────────────────────────
echo ""
info "Setting up Git identity..."
read -p "  Enter your GitHub username: " GH_USER
read -p "  Enter your GitHub email:    " GH_EMAIL

if [ -z "$GH_USER" ] || [ -z "$GH_EMAIL" ]; then
  err "Username and email are required."
  exit 1
fi

git config user.name  "$GH_USER"
git config user.email "$GH_EMAIL"
ok "Git identity configured"

# ─── STEP 3: INITIALIZE REPO ──────────────────────────────
echo ""
info "Initializing local Git repository..."

if [ ! -d ".git" ]; then
  git init
  ok "Local repository initialized"
else
  warn "Repository already initialized — skipping init"
fi

# ─── STEP 4: CREATE .gitignore ────────────────────────────
cat > .gitignore << 'GITIGNORE'
# Aether Ghost OS — Sensitive files to exclude from version control
ghost_tools/ghost.log
ghost_tools/threats.json
ghost_tools/report.json
ghost_tools/schedule_config.json
ghost_tools/active_proxy.json
__pycache__/
*.pyc
*.pyo
.DS_Store
Thumbs.db
GITIGNORE
ok ".gitignore created (excludes logs, configs, threats database)"

# ─── STEP 5: FIRST COMMIT ─────────────────────────────────
git add .
git commit -m "💀 Aether Ghost OS v1.1.0 — Initial secure release"
ok "First commit created"

# ─── STEP 6: SET REMOTE ───────────────────────────────────
echo ""
echo "  Create a repository on GitHub.com first:"
echo "  1. Go to https://github.com/new"
echo "  2. Name it: aether-ghost-os"
echo "  3. Set it to PRIVATE (protects your source code)"
echo "  4. Do NOT initialize with README — we already have files"
echo "  5. Click 'Create Repository'"
echo ""
read -p "  Paste your GitHub repo URL (HTTPS or SSH): " REPO_URL

if [ -z "$REPO_URL" ]; then
  err "No remote URL provided."
  exit 1
fi

# Remove existing remote if it exists
git remote remove origin 2>/dev/null

git remote add origin "$REPO_URL"
ok "Remote 'origin' set to $REPO_URL"

# ─── STEP 7: SET DEFAULT BRANCH ───────────────────────────
git branch -M main 2>/dev/null || true

# ─── STEP 8: PUSH ─────────────────────────────────────────
echo ""
info "Pushing to GitHub..."
if git push -u origin main; then
  ok "✅ Aether Ghost OS pushed to GitHub!"
  echo ""
  echo -e "  ${GREEN}🎉 SUCCESS! Your repository is live.${NC}"
  echo "  View it at: ${REPO_URL%.git}"
  echo ""
  echo "  📋 Next steps:"
  echo "  1. Go to GitHub → Settings → Pages → Deploy from 'docs' folder"
  echo "     (to host your public marketing site at https://YOURUSERNAME.github.io/aether-ghost-os)"
  echo "  2. Invite collaborators under Settings → Collaborators"
  echo "  3. The repository is PRIVATE — no one can see code without your invite"
  echo ""
else
  echo ""
  err "Push failed. Here are the most common fixes:"
  echo ""
  echo "  ── PROBLEM 1: Authentication error (Username/Password rejected) ──────"
  echo "  GitHub no longer accepts passwords. You must use a Personal Access Token."
  echo "  Solution:"
  echo "    → Go to: https://github.com/settings/tokens"
  echo "    → Click 'Generate new token (classic)'"
  echo "    → Check: repo, workflow"
  echo "    → Copy the token (it starts with 'ghp_')"
  echo "    → Use this token as your password when git asks"
  echo ""
  echo "  ── PROBLEM 2: SSH key not set up ────────────────────────────────────"
  echo "  If you used an SSH URL (git@github.com:...) you need an SSH key."
  echo "  Solution:"
  echo "    → Run: ssh-keygen -t ed25519 -C \"$GH_EMAIL\""
  echo "    → Copy the public key: cat ~/.ssh/id_ed25519.pub"
  echo "    → Add it at: https://github.com/settings/keys"
  echo "    → Then retry this script"
  echo ""
  echo "  ── PROBLEM 3: Branch name conflict ─────────────────────────────────"
  echo "  Your GitHub repo may use 'master' not 'main'."
  echo "  Solution:"
  echo "    → Run: git push -u origin master"
  echo ""
  echo "  ── PROBLEM 4: Remote already has commits ────────────────────────────"
  echo "  If the repo was not empty when created."
  echo "  Solution (WARNING — this overwrites remote):"
  echo "    → Run: git push -u origin main --force"
  echo ""
  echo "  ── PROBLEM 5: Termux SSL certificate error ───────────────────────────"
  echo "  Solution:"
  echo "    → Run: pkg install ca-certificates && git config --global http.sslVerify true"
  echo ""
fi
