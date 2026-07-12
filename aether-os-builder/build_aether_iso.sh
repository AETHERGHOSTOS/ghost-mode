#!/usr/bin/env bash
# 💀 AETHER GHOST OS ISO COMPILER SCRIPT
# This script must be run inside an Arch Linux environment (or Ubuntu with Docker/Chroot/WSL).
# It compiles the ISO using the 'archiso' tool suite.

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}💀😈 AETHER GHOST OS ISO BUILDER INITIALISING...${NC}"
echo "=========================================================="

# ── 1. Check root permissions ─────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run this script as root (sudo ./build_aether_iso.sh)${NC}"
    exit 1
fi

# ── 2. Check architecture building dependencies & Docker Fallback ──
if ! command -v mkarchiso &>/dev/null; then
    if command -v pacman &>/dev/null; then
        echo -e "📦 Installing building tools ('archiso')..."
        pacman -S --noconfirm archiso
    else
        # Not on Arch. Check if Docker is installed to run containerised build
        if command -v docker &>/dev/null; then
            echo -e "${GREEN}🐳 Ubuntu/Debian system detected. Docker is installed!${NC}"
            echo -e "   Spawning a privileged Arch Linux container to compile the ISO..."
            echo "   (This handles all dependencies automatically and outputs the ISO locally)"
            echo ""
            
            # Run compilation inside privileged Arch Linux container
            docker run --privileged --rm -v "${BASE_DIR}/..:/workspace" archlinux bash -c "
                echo '🔄 Updating Arch packages and installing archiso...' && \
                pacman -Syu --noconfirm archiso &>/dev/null && \
                echo '🚀 Running ISO compiler inside container...' && \
                cd /workspace/aether-os-builder && \
                ./build_aether_iso.sh
            "
            exit 0
        else
            echo -e "${RED}❌ Building directly on Debian/Ubuntu is not natively supported.${NC}"
            echo "   To build this ISO, you have two choices:"
            echo "   1. Install Docker on your Ubuntu system (recommended):"
            echo "      sudo apt update && sudo apt install -y docker.io"
            echo "      (Once installed, re-run this script and it will build automatically!)"
            echo ""
            echo "   2. Run this script inside a native Arch Linux Virtual Machine."
            exit 1
        fi
    fi
fi

# ── 3. Resolve Workspace directories ──────────────────────────────
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/archiso-aether-work"
OUT_DIR="${BASE_DIR}/out"

rm -rf "${WORK_DIR}"
mkdir -p "${OUT_DIR}"

echo -e "📂 Preparing environment paths..."
echo "   Workspace   : ${BASE_DIR}"
echo "   Working Dir : ${WORK_DIR}"
echo "   Output ISO  : ${OUT_DIR}"

# ── 4. Sync template directory configurations ─────────────────────
# Create local pacman.conf if missing
if [ ! -f "${BASE_DIR}/pacman.conf" ]; then
    echo "⚙️ Creating default package manager config (pacman.conf)..."
    cat > "${BASE_DIR}/pacman.conf" << 'EOF'
[options]
HoldPkg     = pacman glibc
Architecture = auto
Color
CheckSpace
SigLevel    = Required DatabaseOptional
LocalFileSigLevel = Optional

[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

[community]
Include = /etc/pacman.d/mirrorlist
EOF
fi

# ── 5. Copy current Aether Ghost Mode files to the ISO Root ───────
echo -e "🧬 Embedding Aether Ghost Mode source files inside ISO target root..."
DEST_AETHER="${BASE_DIR}/airootfs/usr/share/aether"
rm -rf "${DEST_AETHER}"
mkdir -p "${DEST_AETHER}"

# Copy codebase files, skip builder and work temp directory
cp -r "${BASE_DIR}/../"* "${DEST_AETHER}/" || true
rm -rf "${DEST_AETHER}/aether-os-builder"
rm -rf "${DEST_AETHER}/.git"
rm -rf "${DEST_AETHER}/ghost_tools/quarantine"

# ── 6. Build the live ISO image ───────────────────────────────────
echo -e "${GREEN}🚀 Compiling ISO image files using mkarchiso...${NC}"
echo "   (This downloads Arch packages and compiles the filesystem, please wait...)"
echo ""

mkarchiso -v -w "${WORK_DIR}" -o "${OUT_DIR}" "${BASE_DIR}"

echo ""
echo -e "${GREEN}==========================================================${NC}"
echo -e "${GREEN}✅ SUCCESS! AETHER GHOST OS LIVE ISO GENERATED SUCCESSFULLY!${NC}"
echo -e "📂 Output File: ${OUT_DIR}/aether-ghost-os-v1.0.0.iso"
echo -e "${GREEN}==========================================================${NC}"
echo "Burn the ISO to a USB drive using Rufus (Windows) or BalenaEtcher (macOS/Linux):"
echo "   sudo dd bs=4M if=${OUT_DIR}/aether-ghost-os-v1.0.0.iso of=/dev/sdX conv=fsync oflag=direct status=progress"
echo "=========================================================="
