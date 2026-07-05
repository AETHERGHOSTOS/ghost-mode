#!/bin/bash
# ============================================================
# 💀 AETHER GHOST OS — Universal Installer v1.1.0
# Works on ANY Android phone with Termux
# No root required.
# ============================================================

clear
echo ""
echo "  💀😈🤫  AETHER GHOST OS INSTALLER v1.1.0  🤫😈💀"
echo "  =================================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "  ${CYAN}→  $1${NC}"; }
err()  { echo -e "  ${RED}❌ $1${NC}"; }

# Replace this with your actual GitHub username before pushing
GITHUB_USER="AETHERGHOSTOS"
REPO_NAME="ghost-mode"
BASE="https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/main"

# ─── STEP 1: UPDATE ───────────────────────────────────────
echo -e "${CYAN}[1/6] Updating packages...${NC}"
pkg update -y -o Dpkg::Options::="--force-confnew" > /dev/null 2>&1
ok "Packages updated"

# ─── STEP 2: INSTALL TOOLS ────────────────────────────────
echo -e "${CYAN}[2/6] Installing tools...${NC}"
pkg install -y python nmap net-tools curl tor cronie python-pillow termux-api > /dev/null 2>&1
ok "Installed: python, nmap, curl, tor, cronie, pillow, termux-api"

# ─── STEP 3: PYTHON SETUP ─────────────────────────────────
echo -e "${CYAN}[3/6] Setting up Python...${NC}"
ln -sf $PREFIX/bin/python $PREFIX/bin/python3 2>/dev/null
pip install requests --break-system-packages -q 2>/dev/null
ok "Python and dependencies ready"

# ─── STEP 4: CREATE DIRECTORIES ───────────────────────────
echo -e "${CYAN}[4/6] Creating folders...${NC}"
mkdir -p ~/ghost_tools
mkdir -p ~/.termux
mkdir -p ~/.termux/boot

# Terminal font size configuration (optional)
PROPS="$HOME/.termux/termux.properties"
if ! grep -q "font-size" "$PROPS" 2>/dev/null; then
  echo ""
  echo "  🔤 Terminal Customization:"
  read -p "  Would you like to set the default font size to 12? (y/n) [y]: " font_choice
  if [[ "$font_choice" != "n" && "$font_choice" != "N" ]]; then
    echo "font-size = 12" >> "$PROPS"
    termux-reload-settings 2>/dev/null
    ok "Font size set to 12"
  else
    ok "Kept your custom font configurations"
  fi
fi
ok "Directories and terminal settings audited"

# ─── STEP 5: DOWNLOAD FILES ───────────────────────────────
echo -e "${CYAN}[5/6] Downloading Aether Ghost OS files...${NC}"

download() {
  local url="$1"
  local dest="$2"
  local name="$3"
  
  local local_file=""
  if [ -f "./$name" ]; then
    local_file="./$name"
  elif [ -f "./ghost_tools/$name" ]; then
    local_file="./ghost_tools/$name"
  elif [ -f "./assets/$name" ]; then
    local_file="./assets/$name"
  fi
  
  # Resolve absolute paths to prevent copy-to-self errors
  local abs_local=""
  if [ -n "$local_file" ]; then
    abs_local=$(realpath "$local_file" 2>/dev/null)
  fi
  local abs_dest=$(realpath "$dest" 2>/dev/null)
  
  if [ -n "$abs_local" ] && [ "$abs_local" != "$abs_dest" ]; then
    cp "$abs_local" "$abs_dest" 2>/dev/null && ok "$name (local)" || warn "$name copy failed"
  else
    curl -sL "$url" -o "$dest" 2>/dev/null && ok "$name" || warn "$name download failed"
  fi
}

download "$BASE/ghost_mode.py"                    ~/ghost_mode.py                         "ghost_mode.py"
download "$BASE/ghost.sh"                         ~/ghost.sh                              "ghost.sh"
download "$BASE/ghost_tools/location_picker.py"   ~/ghost_tools/location_picker.py        "location_picker.py"
download "$BASE/ghost_tools/ghost_dashboard.html" ~/ghost_tools/ghost_dashboard.html      "ghost_dashboard.html"
download "$BASE/ghost_tools/server_daemon.py"     ~/ghost_tools/server_daemon.py          "server_daemon.py"
download "$BASE/ghost_tools/render_logo.py"       ~/ghost_tools/render_logo.py            "render_logo.py"
download "$BASE/assets/aether_emoji.png"          ~/ghost_tools/aether_emoji.png          "aether_emoji.png"
download "$BASE/assets/logo.png"                  ~/ghost_tools/logo.png                  "logo.png"

# PC Edition (optional)
download "$BASE/ghost_mode_pc.py" ~/ghost_mode_pc.py "ghost_mode_pc.py (PC Edition)"

# Support Bot (optional)
download "$BASE/support_bot.py" ~/support_bot.py "support_bot.py"

chmod +x ~/ghost.sh

# ─── STEP 6: AUTO-BOOT SETUP ──────────────────────────────
echo -e "${CYAN}[6/6] Setting up auto-boot...${NC}"

# Termux:Boot script — runs when phone boots
cat > ~/.termux/boot/aether_autostart.sh << 'BOOT_EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Aether Ghost OS — Auto-start on phone boot
# Requires: Termux:Boot app from F-Droid

# Wait for system to settle
sleep 8

# Start Tor in background
tor > /dev/null 2>&1 &

# Start cron daemon for scheduled scans
crond

# Start dashboard server
python3 ~/ghost_tools/server_daemon.py > /dev/null 2>&1 &

# Run initial scan after 20 seconds
sleep 20
python3 ~/ghost_mode.py >> ~/ghost_tools/ghost.log 2>&1
BOOT_EOF
chmod +x ~/.termux/boot/aether_autostart.sh
ok "Auto-boot configured (requires Termux:Boot app from F-Droid)"

# ─── SETUP CRON (AUTO-SCAN) ───────────────────────────────
crond 2>/dev/null
(crontab -l 2>/dev/null | grep -v ghost_mode; \
 echo "*/2 * * * * python3 ~/ghost_mode.py >> ~/ghost_tools/ghost.log 2>&1") | crontab -
ok "Auto-scan every 2 minutes configured"

# ─── COPY ASSETS ──────────────────────────────────────────
cp ~/ghost_tools/ghost_dashboard.html /sdcard/Download/ghost_dashboard.html 2>/dev/null
cp ~/ghost_tools/logo.png /sdcard/Download/aether_logo.png 2>/dev/null

echo ""
echo -e "${GREEN}  =================================================="
echo -e "  💀 AETHER GHOST OS v1.1.0 INSTALLED!"
echo -e "  ==================================================${NC}"
echo ""
echo "  Launch:       bash ~/ghost.sh"
echo "  Dashboard:    http://localhost:8080/ghost_dashboard.html"
echo "  PC Edition:   python3 ~/ghost_mode_pc.py"
echo ""
echo -e "${YELLOW}  ⚠️  IMPORTANT NOTE ON TERMUX:API FOR PHONE INTEGRATION:${NC}"
echo "  If commands like 'Test Alarm' or launcher scripts freeze, it means"
echo "  the Termux:API companion app is missing or has a signature mismatch."
echo "  To resolve this:"
echo "  1. Download the \"Termux:API\" APK from F-Droid or GitHub."
echo "  2. Ensure BOTH your Termux app and Termux:API app are from the same source (F-Droid)."
echo "  3. Open Android App Settings ➔ Termux (and Termux:API) ➔ Grant all permissions"
echo "     (especially background access, notifications, and logs/SMS if prompted)."
echo ""
echo -e "${CYAN}  📱 FOR AUTO-BOOT TO WORK:${NC}"
echo "  Install 'Termux:Boot' from F-Droid"
echo "  Open it once to enable boot permission"
echo "  Ghost OS will then start automatically on every reboot"
echo ""
echo -e "${YELLOW}  ⚠️  For personal security and educational use only.${NC}"
echo ""
