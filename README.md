# 💀 Ghost Mode (AetherGhost Guard v1.2.0)

> *Active Defense. Anonymity Routing. Memory Whitelisting. Auto-Updates. Any Android & PC. No root.*

Ghost Mode is a unified, sovereign privacy and security ecosystem designed to secure all your personal devices and networks. It runs locally and sandbox-isolated inside user-space, focusing on active malware/virus scanning, network deception (honeypots), complete anonymity routing, and absolute digital sovereignty without requiring root access or sending your data to any cloud servers.

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-aetherghost.os-orange?style=flat-square&logo=buy-me-a-coffee)](https://buymeacoffee.com/aetherghost.os) [![Bitcoin](https://img.shields.io/badge/Crypto-Accepted-yellow?style=flat-square&logo=bitcoin)](https://github.com/AETHERGHOSTOS/ghost-mode#-support--donate)

---

## 🤔 Why Ghost Mode?

Most security suites are either too complex (built only for enterprise networks or expert laptops) or too restricted (like basic mobile VPNs). Ghost Mode is different — it is a cross-platform, user-space defensive shield that secures both your mobile devices (via Termux on Android) and your computer workstations (via native Python engines on Windows, Linux, and macOS) against stalkerware, spyware, rogue active process backdoors, infected files, and unauthorized network scans. It is built for anyone who wants sovereign protection across all their hardware, without needing complex setups or administrative root access.

---

---

## 🌐 Live Website

**[aetherghostos.github.io/aether-ghost-os-corp](https://aetherghostos.github.io/aether-ghost-os-corp)**

---

## 📊 Global OS Compatibility Matrix

| Feature / Module | Android (Termux) | Windows PC | Linux (Ubuntu/Debian) | macOS |
| :--- | :---: | :---: | :---: | :---: |
| **🛡️ AetherGhost Guard (Virus/Malware)** | ✅ Yes (Stalkerware audit) | ✅ Yes (Defender / Memory whitelist) | ✅ Yes (ClamAV / Memory whitelist) | ✅ Yes (ClamAV / Memory whitelist) |
| **🎙️ Privacy Sentry (Mic/Cam Monitor)** | ✅ Yes (Logcat Audit) | ✅ Yes (Win32 API) | ✅ Yes (lsof/procfs) | ✅ Yes (AVFoundation) |
| **🛡️ Deception Sentry (SSH Honeypot)** | ✅ Yes (Port 2222) | ✅ Yes (Port 2222) | ✅ Yes (Port 2222) | ✅ Yes (Port 2222) |
| **🌐 Sovereign Tor Routing** | ✅ Yes (Tor daemon) | ✅ Yes (Tor service) | ✅ Yes (Tor daemon) | ✅ Yes (Tor daemon) |
| **💬 Scam Sentry (SMS/Clipboard)** | ✅ Yes (SMS / Copy) | ✅ Yes (Clipboard scan) | ✅ Yes (Clipboard scan) | ✅ Yes (Clipboard scan) |
| **🔄 Failover Daemon** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **🖥️ Web Dashboard Console** | ✅ Yes (Port 8080) | ✅ Yes (Port 8080) | ✅ Yes (Port 8080) | ✅ Yes (Port 8080) |
| **⏰ Automated Sentry Alerts** | ✅ Yes (Telegram Sentry) | ✅ Yes (Telegram Sentry) | ✅ Yes (Telegram Sentry) | ✅ Yes (Telegram Sentry) |

---

## 💀 Core Modules

| Module | What it protects you from |
|--------|--------------------------|
| **🎙️ Privacy Sentry** | Monitors Android camera and microphone log access in real-time, preventing spy apps from recording you. |
| **🛡️ Deception Sentry** | Traps and delays unauthorized network scans on port `2222` with a decoy SSH tarpit honeypot, reporting intrusions instantly. |
| **🛡️ AetherGhost Guard** | Cross-platform active scanner checking memory backdoors (Virus Guard) and storage files/Defender/spyware packages (Malware Guard), with remote Telegram Sentry remediation controls. |
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
| **CalyxOS / DivestOS** | 🟢 **Full (Recommended)** | Runs via **Termux** (Pre-installed microG or sandboxed services) | Privacy-focused operational setups |
| **LineageOS** | 🟢 **Full** | Runs via **Termux** (Supports custom ROM system services) | Deloaded open-source mobile setups |
| **Windows 10 / 11** | 🟢 **Full** | Native Python engine (`ghost_mode_pc.py`) | Desktop workstation monitoring |
| **Windows WSL** | 🟢 **Full** | Runs in Windows Subsystem for Linux (WSL Ubuntu/Debian) | Developer environments |
| **Linux (Ubuntu/Debian)** | 🟢 **Full** | Native terminal daemon | General Linux security & servers |
| **Parrot Security OS / Kali**| 🟢 **Full** | Native terminal (Pre-installed security dependencies) | Advanced security environments |
| **macOS (Intel & M-Series)** | 🟢 **Full** | Native terminal via Homebrew | Apple developer workstations |
| **Raspberry Pi OS** | 🟢 **Full** | Native lightweight background daemon | Physical hardware security node |
| **iPhone / iOS** | 🔴 **Unsupported** | Blocked by iOS App Sandbox restrictions | None (Unless jailbroken) |

---

## ⚡ Installation & Quick Start

### 🤖 Option 1: Android (GrapheneOS, CalyxOS, DivestOS, LineageOS)

#### Step 1: Install Termux on your phone
> [!WARNING]
> Do **NOT** install Termux from the Google Play Store (it is outdated and package installations will fail).

* **If F-Droid is working:** Download the [Termux app directly on F-Droid](https://f-droid.org/packages/com.termux/).
* **If F-Droid is down or failing to download:**
  1. Go to the official **[Termux GitHub Releases](https://github.com/termux/termux-app/releases)**.
  2. Scroll down to the latest assets and download the `.apk` file (labeled `universal` or `arm64-v8a`).
  3. Install the downloaded APK file manually on your phone.

> [!NOTE]
> **For Hardened ROMs & Custom OS Profiles (GrapheneOS, CalyxOS, DivestOS, LineageOS):** 
> * You can install Termux in your primary profile or inside a dedicated secondary **"Secure / Guest Profile"** to keep your security suite completely isolated.
> * Ensure you grant Termux **Network** permission in your settings so it can download tool packages and route IPs via Tor.

#### Step 2: Install Ghost Mode
Open Termux and run the universal setup installer:
```bash
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh | bash
```

---

### 🪟 Option 2: Windows PCs & Workstations (All Versions)

#### 🔰 Method A: Download ZIP (Easiest for Beginners — No Git Required)
1. **Install Python:** Download and install Python 3 from [python.org/downloads](https://www.python.org/downloads/). *Check the box **"Add Python to PATH"** before clicking install.*
2. **Download & Extract:**
   * Click this link to download the project: **[Direct ZIP Download Link](https://github.com/AETHERGHOSTOS/ghost-mode/archive/refs/heads/main.zip)**
   * Extract the ZIP folder to your Desktop.
3. **Run:**
   * Double-click **`run_scanner.bat`** to run the scanner.
   * Double-click **`run_dashboard.bat`** to run the local server and open the web dashboard.

#### 💻 Method B: Clone via PowerShell & Git (Advanced)
1. Open PowerShell and clone the project:
   ```powershell
   git clone https://github.com/AETHERGHOSTOS/ghost-mode.git
   cd ghost-mode
   python ghost_mode_pc.py
   ```

#### 🐧 Method C: Windows Subsystem for Linux (WSL)
1. Open PowerShell as Administrator and run: `wsl --install`
2. Reboot your computer, search for "Ubuntu" in your Start Menu, and follow the Linux setup guide below.

---

### 🐧 Option 3: Linux (Ubuntu, Debian, Arch)

#### 🔰 Method A: Download ZIP (Easiest — No Git Required)
1. Open terminal and run this single command line to download and unzip:
   ```bash
   curl -L https://github.com/AETHERGHOSTOS/ghost-mode/archive/refs/heads/main.zip -o ghost-mode.zip && unzip ghost-mode.zip && cd ghost-mode-main
   ```
2. Install dependencies:
   * **Ubuntu/Debian**: `sudo apt update && sudo apt install -y python3 python3-pip nmap tor curl`
   * **Arch Linux**: `sudo pacman -Syy python python-pip nmap tor curl`
3. Run the PC security scanner:
   ```bash
   python3 ghost_mode_pc.py
   ```

#### 💻 Method B: Clone via Git (Advanced)
```bash
git clone https://github.com/AETHERGHOSTOS/ghost-mode.git
cd ghost-mode
pip install requests --break-system-packages
chmod +x ghost.sh
python3 ghost_mode_pc.py
```

---

### 🦜 Option 4: Parrot Security OS & Kali Linux

#### 🔰 Method A: Download ZIP (Easiest — No Git Required)
1. Open terminal and run:
   ```bash
   curl -L https://github.com/AETHERGHOSTOS/ghost-mode/archive/refs/heads/main.zip -o ghost-mode.zip && unzip ghost-mode.zip && cd ghost-mode-main
   ```
2. Run the PC scanner:
   ```bash
   python3 ghost_mode_pc.py
   ```

#### 💻 Method B: Clone via Git (Advanced)
```bash
git clone https://github.com/AETHERGHOSTOS/ghost-mode.git
cd ghost-mode
chmod +x ghost.sh
python3 ghost_mode_pc.py
```

---

### 🍏 Option 5: macOS

#### 🔰 Method A: Download ZIP (Easiest — No Git Required)
1. Open terminal and run:
   ```bash
   curl -L https://github.com/AETHERGHOSTOS/ghost-mode/archive/refs/heads/main.zip -o ghost-mode.zip && unzip ghost-mode.zip && cd ghost-mode-main
   ```
2. Install dependencies using **[Homebrew](https://brew.sh/)**:
   ```bash
   brew install python tor nmap curl
   ```
3. Run the PC scanner:
   ```bash
   python3 ghost_mode_pc.py
   ```

#### 💻 Method B: Clone via Git (Advanced)
```bash
git clone https://github.com/AETHERGHOSTOS/ghost-mode.git
cd ghost-mode
brew install python tor nmap curl
pip install requests
chmod +x ghost.sh
python3 ghost_mode_pc.py
```

---

### 🍓 Option 6: Raspberry Pi OS

#### 🔰 Method A: Download ZIP (Easiest — No Git Required)
1. Open terminal and run:
   ```bash
   curl -L https://github.com/AETHERGHOSTOS/ghost-mode/archive/refs/heads/main.zip -o ghost-mode.zip && unzip ghost-mode.zip && cd ghost-mode-main
   ```
2. Install dependencies:
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip nmap tor curl
   ```
3. Run:
   ```bash
   python3 ghost_mode_pc.py
   ```

#### 💻 Method B: Clone via Git (Advanced)
```bash
git clone https://github.com/AETHERGHOSTOS/ghost-mode.git
cd ghost-mode
sudo apt update && sudo apt install -y python3 python3-pip nmap tor curl
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
  👻 A E T H E R   G H O S T   O S  v1.2.0 👻
  =============================================
  Privacy Operating Security Suite for Termux

  [1] 👻 Select Anonymity Engine
  [2] 🛡️ AetherGhost Guard Scans
  [3] 💀 Run Full System Security Audit
  [4] 🌍 Pick Tor Location Node
  [5] 🌐 Check My Connection
  [6] 🖥️  Open Dashboard
  [7] 📋 View System Logs
  [8] 🔧 Change DNS Resolver
  [9] 🚨 PANIC — Self Destruct
  [10] ⏹️  Stop Everything & Exit
  [12] 🚪 Exit Menu (Keep Services Running)
  [0] 🔤 Reset Termux Font
  [11] ☕ Support & Donate to Project
```

### 🖥️ On Desktop (Windows, macOS, Linux, Parrot, Raspberry Pi)
Run the dedicated PC security engine directly:
```bash
python ghost_mode_pc.py
```
This starts the real-time background monitor, checks active webcam/microphone status, logs local scanning activities, and boots up the browser dashboard integration.

## 🔄 Checking for Updates & Upgrading

To keep your security modules, memory scanners, and threat signatures up to date, Aether OS features an **Automated Self-Updater** alongside traditional manual git pulls.

### 🔍 1. How to Check Your Current Version Status
*   **Via the Dashboard UI:** Look at the version badge in the local web dashboard header (which should display **`v1.2.0`** or higher) and compare it with the latest release.
*   **Via the Telegram Sentry Bot:** Send `/menu` or `/status` to your Sentry Bot. The status response will show the version number and active scan scheduler settings.
*   **Via Git (CLI check):** Open your terminal inside the project directory and run:
    ```bash
    git fetch && git status
    ```
    If updates are available, git will display:  
    `Your branch is behind 'origin/main' by X commits, and can be fast-forwarded.`

---

### 🚀 2. Upgrade Guide for Existing Installations

To apply the latest features, memory scanning engines, and the background Auto-Update engine, follow these step-by-step instructions to upgrade your existing installation.

#### 📱 Step-by-Step for Phones (Android / Termux)
1.  **Open Termux** on your phone.
2.  **Stop all running background services** of your current version:
    ```bash
    pkill -f server_daemon.py
    pkill -f ghost_mode.py
    pkill tor
    ```
3.  **Navigate to the project folder**:
    ```bash
    cd ~/ghost-mode
    ```
4.  **Fetch and pull the latest release files** from GitHub:
    ```bash
    git pull
    ```
5.  **Restart the background daemon**:
    ```bash
    python ghost_tools/server_daemon.py &
    ```
    *Open the dashboard in your mobile browser to verify the green version badge is active in the header!*

#### 🖥️ Step-by-Step for Windows PCs & Workstations (All Versions)
This guide applies to Windows 7, 8, 10, 11, and Windows Server:
1.  **Stop running background processes**:
    *   Close any open black console window running the server or scanner scripts.
    *   Alternatively, open **PowerShell** and run this command to force-close old processes:
        ```powershell
        Stop-Process -Name "python" -Force
        ```
2.  **Navigate to your project directory**:
    *   If installed via Git, open **PowerShell**, go to your folder, and pull:
        ```powershell
        cd C:\Users\Administrator\Downloads\Compressed\ghost-mode\ghost-mode
        git pull
        ```
    *   If installed via a **ZIP Folder**, simply download the latest ZIP folder from your GitHub repository, extract it, and copy/paste all contents into the old folder, overwriting the old files.
3.  **Run the update fully**:
    *   Double-click **`run_dashboard.bat`** (to start the console dashboard server).
    *   Double-click **`run_scanner.bat`** (to start the PC security scanner).
    *   *The browser will open showing the updated dashboard with the latest version badge in the header!*

#### 🍏 Step-by-Step for macOS Computers (Intel & M-Series Silicon)
1.  **Stop background daemons**:
    *   Open Terminal and force kill python processes on your ports:
        ```bash
        pkill -f server_daemon.py
        pkill -f ghost_mode_pc.py
        ```
2.  **Pull updates**:
    *   Navigate to your local repository folder and pull:
        ```bash
        cd ~/ghost-mode
        git pull
        ```
3.  **Restart the security suite**:
    *   Start the server daemon: `python3 ghost_tools/server_daemon.py &`
    *   Start the macOS hardware/memory scanner: `python3 ghost_mode_pc.py &`

#### 🐧 Step-by-Step for Linux Systems (Ubuntu, Debian, Arch, Parrot, Pi)
1.  **Kill running background services**:
    ```bash
    pkill -f server_daemon.py
    pkill -f ghost_mode_pc.py
    pkill tor
    ```
2.  **Pull updates**:
    ```bash
    cd ~/ghost-mode
    git pull
    ```
3.  **Launch the security suite**:
    ```bash
    python3 ghost_tools/server_daemon.py &
    python3 ghost_mode_pc.py &
    ```

---

### ⚙️ 3. How the Auto-Update Engine Works

Once you have upgraded to **`v1.2.0`**, you can manage updates automatically:
*   **Auto-Update Enabled (ON):** The background daemon checks for new GitHub updates every hour. If it finds any, it pulls them automatically, sends a Telegram alert, and executes a hot-restart of the daemon silently.
*   **Auto-Update Disabled (OFF):** The system notifies you of an update via the dashboard or Sentry Bot. You must manually click the **`📥 PULL LATEST`** dashboard button or trigger the manual update inline button inside Telegram Sentry to download and apply changes.

---

## 🧹 Step-by-Step Clean Reset & Reinstallation Guide

If your installation is frozen, buggy, has permission errors, or you simply want to wipe everything clean and start completely fresh, follow these step-by-step instructions for your specific platform.

### 📱 Path A: For Mobile Devices (Android / Termux)

#### 🛑 Phase 1: Wiping & Deleting Clean
1. **Kill background processes:**
   Open Termux and terminate the active server, scanner daemon, Tor, and cron schedulers:
   ```bash
   pkill -f server_daemon.py
   pkill -f ghost_mode.py
   pkill tor
   pkill cron
   ```
2. **Wipe project directories:**
   Delete all configurations, executable scripts, dashboard templates, and logs:
   ```bash
   rm -rf ~/ghost-mode ~/aether-ghost-os ~/ghost_tools
   rm -f ~/ghost.sh ~/ghost_mode.py ~/setup.sh
   ```
3. **Hard Reset (Optional):**
   If packages are totally broken, go to Android Settings ➔ Apps ➔ Termux ➔ Storage ➔ **Clear Storage / Data** to factory reset Termux.

#### 📥 Phase 2: Fresh Installation & Launch
1. Ensure Termux is installed from F-Droid (not Google Play).
2. Set up storage access: `termux-setup-storage` and accept the popup.
3. Download and run the installer (replace `AETHERGHOSTOS` with your real GitHub handle):
   ```bash
   curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
   ```
4. Grant Mic/Cam auditing permission: Connect to a PC with USB debugging on, and run:
   ```bash
   adb shell pm grant com.termux android.permission.READ_LOGS
   ```

---

### 🖥️ Path B: For PC & Desktop Systems (Windows, Linux, macOS)

#### 🛑 Phase 1: Wiping & Deleting Clean
*   **On Windows:**
    1. Close any running command windows showing `ghost_mode_pc.py` or the Python daemon.
    2. Open PowerShell and force-close any locking processes: `Stop-Process -Name "python" -Force`
    3. Delete the repository folders and local tool config:
       ```powershell
       Remove-Item -Path "$HOME\ghost-mode", "$HOME\aether-ghost-os", "$HOME\.ghost_tools" -Recurse -Force -ErrorAction SilentlyContinue
       ```
*   **On Linux / macOS:**
    1. Open your terminal and kill running daemons: `pkill -f ghost_mode_pc.py`
    2. Wipe the folders: `rm -rf ~/ghost-mode ~/aether-ghost-os ~/.ghost_tools`

#### 📥 Phase 2: Fresh Installation & Launch
1. Make sure Python 3 is installed on your computer.
2. Clone or download your repository from GitHub.
3. Open a Command Prompt or Terminal inside the repository folder and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the security engine:
   ```bash
   python ghost_mode_pc.py
   ```

---

## 🔄 Reboot & Power-Off Recovery Guide

If your device or machine loses power, shuts down, or restarts, follow these quick steps to get Aether Ghost OS back up and running.

### 📱 On Android (Termux)
1. Reopen the **Termux** app on your phone.
2. Launch the launcher menu:
   ```bash
   bash ~/ghost.sh
   ```
3. Run Option `[5] 🖥️ Open Dashboard` to start the web console daemon, then select Option `[1] 💀 Run Security Scan` to restart background threat scanning.
4. **💡 Automation Tip:** You can install the **Termux:Boot** addon app from F-Droid and add `bash ~/ghost.sh --boot` to your `~/.termux/boot/` script to start Aether automatically whenever your phone boots up!

### 🖥️ On Desktop PC (Windows, Linux, macOS)
1. Open your terminal, command prompt, or PowerShell.
2. Navigate to your project folder:
   ```bash
   cd ~/ghost-mode
   ```
3. Launch the engine:
   ```bash
   python ghost_mode_pc.py
   ```
4. **💡 Automation Tip:** On Windows, you can add a shortcut of `ghost_mode_pc.py` to your Startup folder (`shell:startup`) to launch Aether automatically on login. On Linux, you can configure a systemd service file.

---

## 💬 Automated Scam Scanning Add-on

Aether Ghost OS can be upgraded to scan incoming messages and clipboard text automatically in the background, rather than requiring you to copy-paste them manually.

### 📱 Android Background Scan (Requires Termux:API)
If you install the **Termux:API** companion app from F-Droid and run the setup script, the Sentry gains these features:
*   **Automated SMS Audits:** Direct access to incoming SMS databases. Any incoming SMS text will be automatically parsed by the Sentry bot, sending you a Telegram notification warning if a phishing link or scam message is detected.
*   **Phone Notifications:** Native Android popup notifications on your lock screen when network threats are detected.

### 🖥️ PC Background Scan (Requires Clipboard Access)
On desktop platforms, Aether runs clipboard loop hooks:
*   **Instant Clipboard Audit:** Whenever you copy any text or URL to your clipboard, Aether automatically inspects the domain for spoofing (e.g. `paypa1.com`) or high-risk TLDs, instantly showing a tray notification bubble if it is unsafe!

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
Some sites (streaming services, banking apps) block known Tor exit nodes. For regular browsing and anonymity, Tor works well. You can pair it with a commercial VPN or custom proxies for layered protection. Note: We are currently developing our own sovereign VPN/proxy routing network (Aether Tunnel) to bypass Tor blocks natively!

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

| **🛡️ Memory Scan** | Triggered scan command or inline button click | `"🛡️ AETHERGHOST GUARD ALERT: Rogue process PID 4102 running unauthorized listening port 4444."` |
| **🛡️ Storage Scan** | Triggered scan command or inline button click | `"🛡️ AETHERGHOST GUARD ALERT: Infected File detected in download folder: backdoor.exe"` |
| **⚡ Threat Resolution** | Callback button `⚡ Resolve Threat 1` | `"✅ Threat Remediation Success: Successfully terminated process PID 4102. Running validation scan..."` |
| **🔄 Auto-Update** | Periodic check trigger or manual override | `"✅ Aether OS Auto-Update: System updated to version v1.2.0 and hot-reloaded successfully!"` |
| **🚨 Intrusion Detection** | Real-time push notification | `"🚨 Intrusion Alert! Decoy Honeypot port scan detected from IP 192.168.1.15."` |
| **🚨 Security Threat** | Threat Alert | `"⚠️ Threat Alert! Microphones currently in use by background process: SpywareAgent"` |
| **🔄 Failover Routing** | Status Alert | `"🔄 Anonymity Pivot: Tor tunnel connection lost. Failover engine WARP connect succeeded."` |
| **💬 Forwarded Phishing link** | Domain Risk Analysis | **🔴 HIGH RISK:** `"❌ paypa1-verification.xyz — Lookalike domain spoofing PayPal with high-risk TLD etc."` |
| **💬 Forwarded SMS scam text** | Text Keyword Audit | **🔴 HIGH RISK:** `"Urgency/Fraud Language Detected (lottery winner, reference codes etc )."` |
| **💬 Forwarded Safe message** | Domain Verification | **🟢 LOW RISK:** `"✅ .com or any other — Recognized domain. No scam indicators detected."` |

### 🕹️ Remote Bot Controls & Commands (v1.2.0+)

The Telegram Sentry Bot provides a full-featured remote management console for your security suite. 

#### 💬 Chat Commands:
* `/menu` — Opens the **Interactive Remote Control Menu** (described below).
* `/status` — Fetches current version (`v1.2.0`), anonymity status, spoofed IP/location, active DNS resolver, scheduler profile, and active threat alarms.
* `/virus` — Remotely triggers an active memory process and open network ports whitelist sweep on-demand.
* `/malware` — Remotely triggers a storage directory, ClamAV, and mobile package scan on-demand.
* `/panic` — Remotely terminates all active background daemons, honeypots, and disconnects all ports.

#### 🎛️ Interactive Keyboard Menu (`/menu`):
When you run `/menu`, you can click inline buttons to perform advanced tasks remotely:
*   **🦠 Scan Memory & 💾 Scan Storage:** Run targeted Virus Guard or Malware Guard scans instantly.
*   **⏳ Scheduler Mode:** Swap monitoring modes between **Time Intervals** (every 2 min, 10 min, 1 hr, 24 hr) or **Daily Scheduled Time** (e.g. 02:00, 22:00).
*   **🔄 Auto-Update Toggle:** Switch between automatic background software updates or manual validation.
*   **📥 Pull Updates:** Check live GitHub repository branch version status and trigger manual `📥 Pull Latest` with zero-downtime hot-restarting.
*   **📋 View Threat Logs & ⚡ Resolve Threat:** Lists active threats with inline resolution buttons. Tapping `⚡ Resolve Threat` immediately terminates rogue PIDs, quarantines malicious files, or uninstalls spyware packages on the remote device.

---

### 📡 Automatic Background Scan Alerts
The Sentry Bot will automatically send an alert message to your Telegram chat after *every* scheduled background scan completes (runs every 2 minutes):
* **Clean Scan:** Sends a confirmation confirming all systems are secure and anonymity layers are holding (e.g. `All Systems Secure (0 threats found). Anonymity layers holding. 👻`).
* **Threat Detected:** Sends a warning showing how many threats were detected, with a recommendation to check the visual dashboard or send `/menu` to audit the issues.

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

# Install latest files from GitHub (replace AETHERGHOSTOS with your repo handle)
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh

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

#### 🛠️ Sentry Bot Troubleshooting & Connection Diagnostics

If your Telegram Sentry Bot is completely silent and does not respond to `/status` or `/scan` commands, follow this diagnostic guide based on your operating system:

##### 1. Understanding the Telegram Chat ID
*   **⚠️ Crucial Concept:** Your **Chat ID is your personal Telegram User ID**. It is **not** unique to a specific bot.
*   Your personal Chat ID is a single, unique numerical string that represents **your Telegram account**. It is the **exact same number** for Sentry Bot, Support Bot, or any utility bot.
*   If you enter the wrong Chat ID or use letters (like your `@username`) in the configuration, the bot will **silently ignore all commands** for safety to prevent unauthorized users from hijacking your device console!
*   **How to get it:** Open Telegram, search for **`@GetIDBot`** or **`@userinfobot`**, tap **Start**, and copy the numerical User ID (e.g. `7636054971`).

##### 2. Diagnostic Steps by Operating System

*   **📱 On Mobile (Android / Termux):**
    1.  **Check if Sentry Settings saved correctly:**
        Run `cat ~/ghost_tools/telegram_config.json` in Termux. It should display your token, chat ID, and `"enabled": true`. If the file is missing or disabled, run this command to create it manually:
        ```bash
        cat > ~/ghost_tools/telegram_config.json << 'EOF'
        {
          "enabled": true,
          "token": "YOUR_BOT_TOKEN",
          "chat_id": "YOUR_CHAT_ID"
        }
        EOF
        ```
    2.  **Inspect connection error logs:**
        Run `cat ~/ghost_tools/ghost.log` or choose Option `[6] 📋 View Logs` in the launcher menu. Check for lines stating `⚠️ Telegram alert failed: <reason>`. A timeout indicates Tor routing blocks or no internet connection.
    3.  **Ensure the daemon server is running:**
        The bot poller only works if Option `[5] 🖥️ Open Dashboard` is actively running. Restart the server daemon:
        ```bash
        pkill -f server_daemon.py
        bash ~/ghost.sh   # select option 5
        ```

*   **🖥️ On Desktop PC (Windows):**
    1.  **Locate your local settings file:**
        Open File Explorer and navigate to `C:\Users\YOUR_USER\.ghost_tools\telegram_config.json` (or look in your project directory). Verify the token and chat ID.
    2.  **Verify background python processes:**
        Open PowerShell and check if the PC engine is active: `Get-Process | Where-Object { $_.Name -eq "python" }`.
    3.  **Check logs:** Open `ghost_tools\ghost.log` inside your project directory to inspect socket timeout errors.

*   **🖥️ On Desktop PC (Linux / macOS):**
    1.  **Locate settings:** Check `~/.ghost_tools/telegram_config.json` (or your project directory).
    2.  **Restart the daemon:** Run `pkill -f ghost_mode_pc.py && python3 ghost_mode_pc.py` in your terminal.
    3.  **Check logs:** Review `~/ghost_tools/ghost.log` or `ghost_tools/ghost.log`.

### 💻 Cross-Platform OS Troubleshooting & Diagnostics (Android, Windows, WSL, Linux, macOS)

If you are running Aether OS on a mobile phone (Android/Termux) or a computer (Windows, Windows Subsystem for Linux (WSL), Linux, or macOS), you might encounter standard configuration edge-cases. Use this diagnostic guide to resolve them:

#### 1. Termux package installation network errors (Android)
* **Issue:** Running `pkg update` or installing python packages inside Termux fails with repository connection timeouts.
* **Fix:** The default Termux mirror might be offline. Switch the repository mirror:
  1. In Termux, run: `termux-change-repo`
  2. Select **Single mirror** ➔ press Enter.
  3. Select the **Cloudflare** or **Grimler** mirror ➔ press Enter.
  4. Run `pkg update -y` again.

#### 2. Background processes terminated / killed by system (Android)
* **Issue:** The Aether daemon silently stops running in the background after some time on Android.
* **Fix:** Android OS kills background terminal apps to save battery. Prevent this by:
  1. Open your phone's **Settings** ➔ search for **Battery Optimization**.
  2. Locate **Termux** and set it to **Don't Optimize / Unrestricted**.
  3. In Termux, run `termux-wake-lock` to keep background services running indefinitely.

#### 3. Logcat Mic/Cam Auditor permission denied (Android)
* **Issue:** Privacy Sentry reports it cannot audit camera or microphone events.
* **Fix:** Termux needs special permission to read system logs:
  1. Connect your phone to your PC and run this ADB command:
     ```bash
     adb shell pm grant com.termux android.permission.READ_LOGS
     ```
  2. Alternatively, if running on custom ROMs, ensure developer logcat auditing is enabled.

#### 4. Command Paste skips steps (Ubuntu WSL)
* **Issue:** Pasting all clone, dependency, and launch commands at once inside WSL skips steps because the first `sudo` command pauses to ask for a password.
* **Fix:** Always copy and paste the installation commands **one line at a time**, waiting for each process to finish before pasting the next.

#### 5. Externally Managed Environment Error (PEP 668)
* **Issue:** When running on Debian/Ubuntu Linux or macOS, `pip install` fails with `error: externally-managed-environment`.
* **Fix:** Tell python to override the standard package manager system rule by appending `--break-system-packages`:
  ```bash
  pip install psutil pysocks --break-system-packages
  ```
  *(Note: The Aether auto-installer handles this dynamically on all Linux/macOS systems).*

#### 6. ModuleNotFoundError immediately after installing dependencies
* **Issue:** You run the scanner, it installs `psutil` or `pysocks` successfully, but then exits with `ModuleNotFoundError: No module named 'psutil'`.
* **Fix:** Python’s running interpreter caches the import path list. Simply **run the scanner command again** (`python3 ghost_mode_pc.py`), and the fresh process will detect and load the packages perfectly.

#### 7. Dashboard buttons return 404/501 errors
* **Issue:** Clicking buttons in the browser returns `404 File Not Found` or `501 Unsupported Method`.
* **Fix:** This means the old static file server is still running on port `8080` from a previous session, blocking the new API server from starting. Kill the old server process to free the port:
  ```bash
  kill -9 $(lsof -t -i:8080) 2>/dev/null || fuser -k 8080/tcp 2>/dev/null
  ```
  Then restart `python3 ghost_mode_pc.py`.

#### 8. Port 8080 already in use by AirPlay Receiver (macOS)
* **Issue:** On macOS Monterey or newer, starting the dashboard server returns `OSError: [Errno 48] Address already in use`.
* **Fix:** Apple runs the "AirPlay Receiver" service on port `8080` by default. You can disable it to free the port:
  1. Open **System Settings** on your Mac.
  2. Go to **General** ➔ **AirDrop & Handoff** (or **Sharing**).
  3. Turn **OFF** the toggle for **AirPlay Receiver**.
  4. Restart your Aether daemon.

#### 9. Permission Denied trying to run script (Linux / macOS)
* **Issue:** Running `./setup.sh` or `./run_dashboard.sh` fails with `Permission denied`.
* **Fix:** Give the script executable permissions before running it:
  ```bash
  chmod +x setup.sh
  chmod +x ghost.sh
  ```

#### 10. Dashboard does not show "Dismiss Alerts" or status badges
* **Issue:** You pulled the latest updates, but the web dashboard still does not show the new buttons or features.
* **Fix:** Your browser has cached the old HTML page. Force the browser to discard cached files and load the fresh updates by performing a **Hard Refresh**:
  * **Windows / Linux PC:** Press **`Ctrl + F5`** (or `Ctrl + Shift + R`).
  * **macOS:** Press **`Cmd + Shift + R`** (Safari: hold `Shift` and click the Reload button).
  * **Android / iOS Mobile:** Clear browser history/site data, or reload in Incognito/Private mode.

#### 11. False positive "External background session detected" alerts
* **Issue:** The security shield detects standard background system tasks (like Ubuntu's `unattended-upgrades`) or your own Telegram Sentry Bot (`support_bot.py`) and lists them as active threats.
* **Fix:** Update your repository using `git pull`. We have whitelisted standard Linux system daemons and the Sentry Bot, and updated the dashboard modal to display dynamic **`🟢 RESOLVED / SAFE`** and **`🔴 STILL ACTIVE`** badges!

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
