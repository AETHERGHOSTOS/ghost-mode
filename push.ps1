Write-Host "============================================="
Write-Host "GHOST MODE - Windows GitHub Setup"
Write-Host "============================================="

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed on this system. Please install Git for Windows (https://git-scm.com/download/win) and retry."
    exit
}

# Initialize Git if needed
if (!(Test-Path .git)) {
    Write-Host "[INFO] Initializing Git repository..."
    git init -b main
} else {
    Write-Host "[INFO] Git repository already initialized."
}

# Add files
Write-Host "[INFO] Adding files to git..."
git add .

# Check if there is anything to commit
$status = git status --porcelain
if ($status) {
    Write-Host "[INFO] Creating commit..."
    git commit -m "Initial commit: Ghost Mode security suite"
    Write-Host "[OK] Commit created."
} else {
    Write-Host "[INFO] No new changes to commit."
}

# Prompt user for GitHub repository URL
Write-Host ""
Write-Host "Create a repository on GitHub.com first:"
Write-Host "1. Go to https://github.com/new"
Write-Host "2. Name it: ghost-mode"
Write-Host "3. Set it to PUBLIC or PRIVATE as desired."
Write-Host "4. Do NOT check README, .gitignore, or License options (keep them off)."
Write-Host "5. Click 'Create Repository'"
Write-Host ""

$repoUrl = Read-Host "Paste your GitHub repository URL (HTTPS or SSH)"
$repoUrl = $repoUrl.Trim()

if ([string]::IsNullOrEmpty($repoUrl)) {
    Write-Error "Repository URL cannot be empty. Setup aborted."
    exit
}

# Set remote origin
git remote remove origin 2>$null
git remote add origin $repoUrl

# Push
Write-Host "[INFO] Pushing to GitHub..."
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Your Ghost Mode repository is live on GitHub!"
} else {
    Write-Host "[ERROR] Push failed. If this is an authentication issue, make sure you are logged in to GitHub."
}
