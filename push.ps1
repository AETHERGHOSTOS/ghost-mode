Write-Host "AETHER GHOST OS - Windows GitHub Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed on this system. Please install Git for Windows (https://git-scm.com/download/win) and retry."
    exit
}
Write-Host "[OK] Git is installed." -ForegroundColor Green

# Git configuration
$gh_user = Read-Host "Enter your GitHub username"
$gh_email = Read-Host "Enter your GitHub email"

if ([string]::IsNullOrEmpty($gh_user) -or [string]::IsNullOrEmpty($gh_email)) {
    Write-Error "Username and Email are required."
    exit
}

git config user.name "$gh_user"
git config user.email "$gh_email"
Write-Host "[OK] Git identity configured." -ForegroundColor Green

# Initialize git
if (-not (Test-Path .git)) {
    git init
    Write-Host "[OK] Local repository initialized." -ForegroundColor Green
} else {
    Write-Host "[WARN] Git repository already initialized." -ForegroundColor Yellow
}

# Create .gitignore
$gitignore_content = @"
# Aether Ghost OS - Sensitive files to exclude from version control
ghost_tools/ghost.log
ghost_tools/threats.json
ghost_tools/report.json
ghost_tools/schedule_config.json
ghost_tools/active_proxy.json
bot_config.json
bot_data.json
__pycache__/
*.pyc
*.pyo
.DS_Store
Thumbs.db
"@
Set-Content -Path .gitignore -Value $gitignore_content -Force
Write-Host "[OK] .gitignore created." -ForegroundColor Green

# Add and Commit
git add .
git commit -m "Aether Ghost OS v1.1.0 - Initial secure release"
Write-Host "[OK] First commit created." -ForegroundColor Green

Write-Host ""
Write-Host "Create a repository on GitHub.com first:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/new"
Write-Host "2. Name it: aether-ghost-os"
Write-Host "3. Set it to PRIVATE (protects your source code from theft)"
Write-Host "4. Do NOT initialize with README - we already have files"
Write-Host "5. Click 'Create Repository'"
Write-Host ""

$repo_url = Read-Host "Paste your GitHub private repo URL (HTTPS or SSH)"
if ([string]::IsNullOrEmpty($repo_url)) {
    Write-Error "Repository URL is required."
    exit
}

# Remove remote if exists
git remote remove origin 2>$null
git remote add origin "$repo_url"
git branch -M main

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS! Your private OS repository is live on GitHub." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Push failed. Common fixes:" -ForegroundColor Red
    Write-Host "1. GitHub no longer accepts passwords. Use a Personal Access Token (PAT):"
    Write-Host "   -> Go to: https://github.com/settings/tokens"
    Write-Host "   -> Click 'Generate new token (classic)'"
    Write-Host "   -> Check: repo, workflow"
    Write-Host "   -> Copy the token (starts with 'ghp_')"
    Write-Host "   -> Use this token as your PASSWORD when Git asks you to log in"
    Write-Host "2. If your remote repository is not empty (contains commits), force push:"
    Write-Host "   -> Run: git push -u origin main --force"
}
