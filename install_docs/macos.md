# Aether Ghost OS — macOS Installation Guide

Run Aether Ghost OS on Apple macOS (Intel or Apple Silicon M1/M2/M3).

## 🛠️ Step 1: Install Homebrew & Sockets
Open Terminal and install packages:
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python nmap tor
```

## 📦 Step 2: Set Up Project
```bash
git clone https://github.com/YOURUSERNAME/aether-ghost-os.git
cd aether-ghost-os
pip3 install psutil requests
```

## 👻 Step 3: Launch Aether
```bash
python3 ghost_mode_pc.py
```
The application will launch the local web server and open the security console in Safari/Chrome.
