#!/bin/bash
# ============================================================
# 💀 AETHER GHOST OS — Universal Installer
# Works on ANY Android phone with Termux
# No root required.
# ============================================================

clear
echo ""
echo "  💀😈🤫  AETHER GHOST OS INSTALLER  🤫😈💀"
echo "  ========================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "  ${CYAN}→  $1${NC}"; }

# ─── STEP 1: UPDATE ───────────────────────────────────────
echo -e "${CYAN}[1/5] Updating packages...${NC}"
pkg update -y -o Dpkg::Options::="--force-confnew" > /dev/null 2>&1
ok "Packages updated"

# ─── STEP 2: INSTALL TOOLS ────────────────────────────────
echo -e "${CYAN}[2/5] Installing tools & styling engines...${NC}"
pkg install -y python nmap net-tools curl tor cronie python-pillow termux-api > /dev/null 2>&1
ok "Tools installed: python, nmap, curl, tor, cronie, python-pillow, termux-api"

# ─── STEP 3: PYTHON SETUP ─────────────────────────────────
echo -e "${CYAN}[3/5] Setting up Python...${NC}"
ln -sf $PREFIX/bin/python $PREFIX/bin/python3 2>/dev/null
pip install requests --break-system-packages -q 2>/dev/null
ok "Python ready"

# ─── STEP 4: CREATE DIRECTORIES & CONFIGS ────────────────
echo -e "${CYAN}[4/5] Creating folders & configuring screen-fit terminal font...${NC}"
mkdir -p ~/ghost_tools
mkdir -p ~/.termux
PROPS_FILE="$HOME/.termux/termux.properties"
if [ -f "$PROPS_FILE" ]; then
  if grep -q "font-size" "$PROPS_FILE"; then
    echo "  → Preserving existing Termux font-size setting."
  else
    echo "font-size = 12" >> "$PROPS_FILE"
    termux-reload-settings 2>/dev/null
  fi
else
  echo "font-size = 12" > "$PROPS_FILE"
  termux-reload-settings 2>/dev/null
fi
ok "Terminal font size configured to auto-fit. Folders created"

# ─── STEP 5: DOWNLOAD FILES FROM GITHUB ───────────────────
echo -e "${CYAN}[5/5] Downloading Aether Ghost OS files...${NC}"

BASE="https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main"

curl -sL "$BASE/ghost_mode.py" -o ~/ghost_mode.py 2>/dev/null && ok "ghost_mode.py" || warn "ghost_mode.py failed"
curl -sL "$BASE/ghost.sh" -o ~/ghost.sh 2>/dev/null && ok "ghost.sh" || warn "ghost.sh failed"
curl -sL "$BASE/ghost_tools/location_picker.py" -o ~/ghost_tools/location_picker.py 2>/dev/null && ok "location_picker.py" || warn "location_picker.py failed"
curl -sL "$BASE/ghost_tools/ghost_dashboard.html" -o ~/ghost_tools/ghost_dashboard.html 2>/dev/null && ok "ghost_dashboard.html" || warn "ghost_dashboard.html failed"
curl -sL "$BASE/ghost_tools/server_daemon.py" -o ~/ghost_tools/server_daemon.py 2>/dev/null && ok "server_daemon.py" || warn "server_daemon.py failed"
curl -sL "$BASE/assets/logo.png" -o ~/ghost_tools/logo.png 2>/dev/null && ok "logo.png" || warn "logo.png failed"

chmod +x ~/ghost.sh

# Copy dashboard and logo to sdcard if possible
cp ~/ghost_tools/ghost_dashboard.html /sdcard/Download/ghost_dashboard.html 2>/dev/null
cp ~/ghost_tools/logo.png /sdcard/Download/logo.png 2>/dev/null && \
  ok "Dashboard and Logo copied to Downloads" || \
  info "Dashboard at: ~/ghost_tools/ghost_dashboard.html"

echo ""
echo -e "${GREEN}  ========================================"
echo -e "  💀 AETHER GHOST OS INSTALLED SUCCESSFULLY!"
echo -e "  ========================================${NC}"
echo ""
echo "  Run anytime:  bash ~/ghost.sh"
echo ""
echo "  Dashboard:    Choose Option 5 in launcher menu"
echo "                (Or visit http://localhost:8080/ghost_dashboard.html)"
echo ""
echo -e "${CYAN}  📱 TO SET A CUSTOM BACKGROUND WALLPAPER IN TERMUX:${NC}"
echo "  1. Install the \"Termux:Styling\" app from F-Droid or GitHub."
echo "  2. Open Termux, long-press anywhere on the terminal window."
echo "  3. Tap \"More...\" ➔ \"Style\" ➔ \"Choose Color/Background\"."
echo "  4. Select your custom wallpaper image from your phone!"
echo ""
echo -e "${YELLOW}  ⚠️  For educational and personal security use only.${NC}"
echo ""
