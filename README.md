# 💀 Ghost Mode

> *Go invisible. Stay protected. Any Android. No root.*

Ghost Mode is a unified, sovereign privacy ecosystem designed to secure all your personal devices and networks. It runs locally and sandbox-isolated inside user-space, focusing on complete privacy and absolute digital sovereignty without requiring root access or sending your data to any cloud servers.

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-aetherghost.os-orange?style=flat-square&logo=buy-me-a-coffee)](https://buymeacoffee.com/aetherghost.os) [![Bitcoin](https://img.shields.io/badge/Crypto-Accepted-yellow?style=flat-square&logo=bitcoin)](https://github.com/AETHERGHOSTOS/ghost-mode#-support--donate)

---

## 🤔 Why Ghost Mode?

Most security tools are built for experts on laptops. Ghost Mode is different — it's built for **anyone** who wants to protect themselves on their phone. One command installs everything. One menu controls everything.

---

## 💀 Core Modules

| Module | What it protects you from |
|--------|--------------------------|
| **🎙️ Privacy Sentry** | Monitors Android camera and microphone log access in real-time, preventing spy apps from recording you. |
| **🛡️ Deception Sentry** | Traps and delays unauthorized network scans on port `2222` with a decoy SSH tarpit honeypot, reporting intrusions instantly. |
| **🌐 Sovereign Tor Routing** | Routes Termux web requests and scans securely through Tor, utilizing country-rotational SOCKS5 proxy circuits. |
| **💬 Scam Sentry** | Offline-compatible link and message scanner running inside Telegram to check incoming SMS for fraud, phishing, and bad links. |
| **🔄 Failover Daemon** | Background loop that tests connection health and automatically rotates between Tor, Cloudflare WARP, and secure DNS. |
| **🖥️ Browser Dashboard** | Interactive local console showing all hardware scan results, speed tests, and log streams. |
| **⏰ Auto-scan** | Lightweight loop that runs silently every 2 minutes in the background, consuming minimal battery. |

---

## 🌍 Global OS Compatibility Matrix

Ghost Mode is built to operate across a wide variety of hardware architectures and operating systems:

| Operating System | Support Level | How it Runs | Best Use Case |
| :--- | :--- | :--- | :--- |
| **Android (6.0+)** | 🟢 **Full (Recommended)** | Runs via **Termux** environment (No root required) | On-the-go mobile defense |
| **GrapheneOS / Pixel** | 🟢 **Full (Recommended)** | Runs via **Termux** (Supports sandboxed user profiles) | Hardened stealth operational device |
| **Windows 10 / 11** | 🟢 **Full** | Native Python engine (`ghost_mode_pc.py`) | Desktop workstation monitoring |
| **Windows WSL** | 🟢 **Full** | Runs in Windows Subsystem for Linux (WSL Ubuntu/Debian) | Developer environments |
| **Linux (Ubuntu/Debian)** | 🟢 **Full** | Native terminal daemon | General Linux security & servers |
| **Parrot Security OS / Kali**| 🟢 **Full** | Native terminal (Pre-installed security dependencies) | Advanced security environments |
| **macOS (Intel & M-Series)** | 🟢 **Full** | Native terminal via Homebrew | Apple developer workstations |
| **Raspberry Pi OS** | 🟢 **Full** | Native lightweight background daemon | Physical hardware security node |
| **iPhone / iOS** | 🔴 **Unsupported** | Blocked by iOS App Sandbox restrictions | None (Unless jailbroken) |

---

## ⚡ Installation & Quick Start

### 🤖 Option 1: Android, Google Pixel & GrapheneOS

#### Step 1: Install Termux on your phone
> [!WARNING]
> Do **NOT** install Termux from the Google Play Store (it is outdated and package installations will fail).

* **If F-Droid is working:** Download the [Termux app directly on F-Droid](https://f-droid.org/packages/com.termux/).
* **If F-Droid is down or failing to download:**
  1. Go to the official **[Termux GitHub Releases](https://github.com/termux/termux-app/releases)**.
  2. Scroll down to the latest assets and download the `.apk` file (labeled `universal` or `arm64-v8a`).
  3. Install the downloaded APK file manually on your phone.

> [!NOTE]
> **For GrapheneOS / Secure Android Profiles:** 
> * You can install Termux in your primary profile or inside a dedicated secondary **"Secure / Guest Profile"** to keep your security suite completely isolated.
> * Ensure you grant Termux **Network** permission in your GrapheneOS settings so it can download tool packages and rotate IPs via Tor.

#### Step 2: Install Ghost Mode
Open Termux and run the universal setup installer:
```bash
curl -sL https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main/setup.sh | bash
```

---

### 🪟 Option 2: Windows (10/11)

#### Method A: Native Python (easiest & simplest)
1. **Install Python:** Download and install Python 3 from the official **[Python Website](https://www.python.org/downloads/)**. *Make sure to check the box: **"Add Python to PATH"** during setup.*
2. **Download & Run:**
   * Clone or download this project folder.
   * Open PowerShell or Command Prompt inside the folder and run:
     ```powershell
     python ghost_mode_pc.py
     ```
   *(The script will automatically detect and install any missing library dependencies like `psutil` and `requests`.)*

#### Method B: Windows Subsystem for Linux (WSL)
1. Open PowerShell as Administrator and install WSL:
   ```powershell
   wsl --install
   ```
2. Open your new Linux Terminal (e.g., Ubuntu) and follow the **Option 3: Linux** instructions below.

---

### 🐧 Option 3: Linux (Ubuntu, Debian, Arch)

1. Open your terminal and install the required security dependencies:
   * **Ubuntu/Debian**:
     ```bash
     sudo apt update && sudo apt install -y python3 python3-pip nmap tor curl
     ```
   * **Arch Linux**:
     ```bash
     sudo pacman -Syy python python-pip nmap tor curl
     ```
2. Clone this repository and configure permissions:
   ```bash
   git clone https://github.com/YOURUSERNAME/ghost-mode.git
   cd ghost-mode
   pip install requests --break-system-packages
   chmod +x ghost.sh
   ```

---

### 🦜 Option 4: Parrot Security OS & Kali Linux

Since Parrot OS and Kali Linux are built specifically for security, they come with dependencies like Python, Tor, and Nmap pre-installed out of the box!
1. Open your terminal and clone the suite:
   ```bash
   git clone https://github.com/YOURUSERNAME/ghost-mode.git
   cd ghost-mode
   pip install requests --break-system-packages 2>/dev/null
   chmod +x ghost.sh
   ```
2. Run the suite:
   ```bash
   python3 ghost_mode_pc.py
   ```

---

### 🍏 Option 5: macOS

1. Open Terminal and install dependencies using **[Homebrew](https://brew.sh/)**:
   ```bash
   brew install python tor nmap curl
   ```
2. Clone this repository and configure:
   ```bash
   git clone https://github.com/YOURUSERNAME/ghost-mode.git
   cd ghost-mode
   pip install requests
   chmod +x ghost.sh
   ```

---

### 🍓 Option 6: Raspberry Pi OS

Perfect for setting up a dedicated security monitor in your house:
1. Open the Raspberry Pi terminal and install tools:
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip nmap tor curl
   ```
2. Clone and run in background mode:
   ```bash
   git clone https://github.com/YOURUSERNAME/ghost-mode.git
   cd ghost-mode
   pip install requests --break-system-packages
   python3 ghost_mode_pc.py
   ```

---

### 🍎 Option 7: iPhone / iOS (Why it is Unsupported)

Due to Apple's strict security model:
* **App Sandboxing:** iOS blocks apps from accessing active system background processes, querying system logs, or monitoring hardware microphone/webcam usage registry entries.
* **Network Restrictions:** Raw TCP/UDP socket creation and network scanning (like Nmap port scans or ARP spoof detection) are heavily blocked.
* **Workaround:** If you have a **jailbroken** device, you can install a terminal emulator (such as NewTerm) and run the Python engine via custom Cydia/Sileo packages, but this is experimental and not officially supported.

---

## 🚀 Usage

Launch the operational suite depending on your device type:

### 📱 On Mobile (Android / Termux)
Run the launcher script:
```bash
bash ~/ghost.sh
```
This opens the terminal dashboard:
```
  💀😈🤫  G H O S T   M O D E  🤫😈💀
  ========================================
  Personal Security Suite for Android

  [1] 💀 Run Security Scan
  [2] 😈 Go Anonymous (Tor)
  [3] 🌍 Pick My Location
  [4] 🌐 Check My IP
  [5] 🖥️  Open Dashboard
  [6] 📋 View Logs
  [7] ⏹️  Stop Everything
```

### 🖥️ On Desktop (Windows, macOS, Linux, Parrot, Raspberry Pi)
Run the dedicated PC security engine directly:
```bash
python ghost_mode_pc.py
```
This starts the real-time background monitor, checks active webcam/microphone status, logs local scanning activities, and boots up the browser dashboard integration.

---

## 🧹 Step-by-Step Clean Reset & Reinstallation Guide

If your installation is frozen, buggy, has permission errors, or you simply want to wipe everything clean and start completely fresh, follow these step-by-step instructions.

### 🛑 Phase 1: Wiping Everything Clean (The Kill & Delete Steps)
We must ensure no hidden background scripts are running or locking directories before we delete them.

1. **Kill all active background services:**
   Open Termux and force-terminate the active server, scanner daemon, Tor, and cron processes:
   ```bash
   pkill -f server_daemon.py
   pkill -f ghost_mode.py
   pkill tor
   pkill cron
   ```
2. **Wipe all files, configurations, and logs:**
   Delete all project folders, scripts, HTML dashboard caches, and log files:
   ```bash
   rm -rf ~/ghost-mode
   rm -rf ~/aether-ghost-os
   rm -rf ~/ghost_tools
   rm -f ~/ghost.sh ~/ghost_mode.py ~/setup.sh
   ```
3. **Reset Termux configuration (Optional but Recommended):**
   If you want to clear Termux styling or reload basic configuration files:
   ```bash
   rm -f ~/.termux/font.ttf
   termux-reload-settings 2>/dev/null
   ```
4. **Clear App Storage (Optional - Hard Reset):**
   If packages are totally broken, go to your phone's Android settings ➔ Apps ➔ Termux ➔ Storage ➔ **Clear Storage / Clear Data**. This resets Termux back to factory defaults.

---

### 📥 Phase 2: Installing Fresh from Scratch (The Build Steps)

1. **Get Termux from F-Droid:**
   If you had to clear data, ensure you are using F-Droid's Termux app, NOT the Google Play Store version (which fails package installation).
2. **Grant Storage Access:**
   Open Termux and run:
   ```bash
   termux-setup-storage
   ```
   Accept the storage permissions popup.
3. **Execute the Setup Installer Script:**
   Download and execute your setup script (replace `YOURUSERNAME` with your real GitHub handle):
   ```bash
   curl -sL https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
   ```
4. **Grant Android Log-Reading Permission:**
   To scan microphone and camera usage without root, connect your phone to a PC with USB debugging enabled, and run this command inside the PC terminal:
   ```bash
   adb shell pm grant com.termux android.permission.READ_LOGS
   ```
   *Note: If the Termux API addon app is not installed or has a signature mismatch, see the warning checklist in the installer output.*

---

### 🚀 Phase 3: Launching & Configuring Sentry Alerts (The Launch & Optional Steps)

1. **Launch the Control Panel:**
   Type the launch command in Termux:
   ```bash
   bash ~/ghost.sh
   ```
2. **Start the background consoles:**
   Select option `[5] 🖥️ Open Dashboard` to start the daemon, then visit `http://localhost:8080/ghost_dashboard.html` in your phone browser.
3. **Set up optional Telegram alerts (Highly Recommended):**
   * Open the dashboard in your mobile browser.
   * Scroll down to the **🤖 Telegram Threat Alerts** card.
   * Enable the alerts checkmark, paste your **Bot API Token** (from `@BotFather`) and your **Chat ID** (from `@userinfobot`).
   * Click **Save Settings** and tap **⚡ Test Sentry** to test your connection!

---

## 🌍 Location Picker

Ghost Mode lets you choose which country your internet traffic appears to come from:

```
  [1]  🇺🇸 United States
  [2]  🇬🇧 United Kingdom
  [3]  🇩🇪 Germany
  [4]  🇳🇱 Netherlands
  ...and 16 more countries
  [0]  🌍 Random (auto)
```

Pick one or multiple countries. Your traffic rotates through them automatically.

---

## 📁 Project Structure

```
ghost-mode/
├── ghost_mode.py          # Main security scanner
├── ghost.sh               # Launcher menu
├── setup.sh               # Universal installer
├── ghost_tools/
│   ├── location_picker.py # Tor country picker
│   └── ghost_dashboard.html # Browser dashboard
├── assets/
│   └── logo.svg           # Ghost Mode logo
└── README.md
```

---

## ❓ Common Questions

**Does it work offline?**
Core scanning (network, mic/camera, ARP, ports) works fully offline. Tor anonymity requires internet.

**Will it drain my battery?**
Ghost Mode is lightweight. The scan runs in under 5 seconds every 2 minutes and uses minimal resources.

**Can websites detect Tor?**
Some sites (Netflix, banking apps) block known Tor IPs. For regular browsing and anonymity, Tor works well. Pair with Surfshark VPN for better results.

**Does my location change automatically?**
Yes — every time you restart Tor or start a new session, you get a different IP. You can also manually pick a location using option 3.

**Can it prevent attacks?**
Ghost Mode detects threats and alerts you. It hides your real IP from attackers. It does not replace a full firewall but provides strong personal protection for everyday use.

---

## ⚠️ Disclaimer

Ghost Mode is built for **personal security, privacy, and education only**.

- ✅ Protect your own device and network
- ✅ Learn about cybersecurity
- ✅ Monitor your own traffic
- ❌ Do not use against others without permission
- ❌ Do not use for illegal activities

The developer takes no responsibility for misuse.

---

## 🛠️ Built With

- Python 3
- Bash
- Tor
- Nmap
- Termux API
- HTML/CSS/JS (dashboard)

---

## 🌍 Similar Tools (and why Ghost Mode is different)

| Tool | Root needed? | Easy setup? | Personal focus? |
|------|-------------|-------------|-----------------|
| Kali NetHunter | ✅ Yes | ❌ Complex | ❌ Offensive |
| cSploit | ✅ Yes | ❌ Complex | ❌ Offensive |
| Wireshark | ❌ No | ❌ PC only | ⚠️ Partial |
| **Ghost Mode** | ❌ **No** | ✅ **One command** | ✅ **Defensive** |

Ghost Mode is the only **no-root, one-command, defensive security suite** designed specifically for everyday Android users who want privacy and protection without being security experts.

---

## 🤖 Optional: Telegram Sentry & Scam Detection Bot

Aether Ghost OS includes a companion Telegram Bot system that sends real-time push alerts to your phone and lets you audit your device remotely or analyze incoming scam messages.

### 🌟 Bot Capabilities & Scenarios

| Trigger / Action | Bot Response | Risk Assessment / Result |
|---|---|---|
| **🚨 Intrusion Detection** | Real-time push notification | `"🚨 Intrusion Alert! Decoy Honeypot port scan detected from IP 192.168.1.15."` |
| **🚨 Security Threat** | Threat Alert | `"⚠️ Threat Alert! Microphones currently in use by background process: SpywareAgent"` |
| **🔄 Failover Routing** | Status Alert | `"🔄 Anonymity Pivot: Tor tunnel connection lost. Failover engine WARP connect succeeded."` |
| **💬 Forwarded Phishing link** | Domain Risk Analysis | **🔴 HIGH RISK:** `"❌ paypa1-verification.xyz — Lookalike domain spoofing PayPal with high-risk TLD."` |
| **💬 Forwarded SMS scam text** | Text Keyword Audit | **🔴 HIGH RISK:** `"Urgency/Fraud Language Detected (lottery winner, m-pesa reference code)."` |
| **💬 Forwarded Safe message** | Domain Verification | **🟢 LOW RISK:** `"✅ safaricom.co.ke — Recognized domain. No scam indicators detected."` |

### 🕹️ Remote Bot Commands (Send to your private bot chat)
* `/status` — Fetches current spoofed IP, anonymity health status, CPU thermalzone temperature, and threat counts.
* `/scan` — Triggers an active hardware/network security shield check instantly and returns the results.
* `/panic` — Remotely kills all Termux logs, decoys, active daemons, and disconnects all ports.

---

### ⚙️ Step-by-Step Setup Guide

#### 1. Generate Your Bot Credentials
1. Open Telegram, search for **`@BotFather`** and start a chat. Send `/newbot` and follow the prompts to get your **Bot Token** (looks like `73829104:AAG9x...`).
2. Search for **`@userinfobot`** on Telegram and click Start to get your numerical **Chat ID** (looks like `583920194`).

#### 2. Install/Update Aether Ghost OS on Phone
Open **Termux** and run:
```bash
# Clean up older background operations
pkill -f server_daemon.py
pkill -f ghost_mode.py
pkill tor
pkill cron

# Clear older versions
rm -rf ~/ghost_tools
rm -f ~/ghost.sh ~/ghost_mode.py ~/setup.sh

# Install latest files from GitHub (replace YOURUSERNAME with your repo handle)
curl -sL https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh

# Run the launcher
bash ~/ghost.sh
```

#### 3. Save Settings & Test
1. Launch Option `5` in the menu (or visit `http://localhost:8080` in your phone browser) to open the dashboard.
2. Scroll to the **Telegram Threat Alerts** panel.
3. Turn on the checkmark, paste your **Token** and **Chat ID**, and click **Save Settings**.
4. Click **Test Sentry**. You will receive an instant verification message on Telegram!

#### 🔑 Token Recovery & Reset Guide

If you lose your Bot API Token, Chat ID, or want to secure your connection, follow these steps:

*   **To Retrieve Your Bot Token:** Open Telegram, open your chat with **`@BotFather`**, send `/token`, select your bot, and copy it.
*   **To Revoke & Refresh Bot Token:** If your token is compromised, send `/revoke` to **`@BotFather`**, select your bot, and it will instantly cancel the old one and generate a fresh token. Update the new token in your dashboard settings.
*   **To Retrieve Your Chat ID:** Open Telegram, search for **`@userinfobot`**, tap Start (or send `/start`), and copy the numerical ID.
*   **To Clear Credentials & Reset Bot:**
    *   *Via Dashboard:* Uncheck "Enable Telegram Alerts", delete the Token and Chat ID values, and click **Save Settings**.
    *   *Via Termux CLI:* Open Termux and run: `rm ~/ghost_tools/telegram_config.json` to delete the settings file directly.

---

## ☕ Support & Donate

Ghost Mode is built and maintained independently. If this tool keeps you safe, consider supporting its development:

### 🌐 Web Donations
| Platform | Link |
|---|---|
| ☕ Buy Me a Coffee | [buymeacoffee.com/aetherghost.os](https://buymeacoffee.com/aetherghost.os) |

### 🪙 Crypto
| Token | Network | Address |
|---|---|---|
| USDT | TRX — Tron (TRC20) | `TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU` |
| USDC | SOL — Solana | `9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui` |
| USDT | ETH — Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| BNB | BSC — BNB Smart Chain (BEP20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| BNB | ETH — Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | BTC — Bitcoin | `15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k` |
| Bitcoin | BSC — BNB Smart Chain (BEP20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | ETH — Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | SEGWIT — BTC (SegWit) | `bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj` |

*Every contribution — no matter how small — keeps Ghost Mode alive and free for everyone.*

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Made with 💀 for privacy.*
