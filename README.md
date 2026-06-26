# 💀 Ghost Mode

> *Go invisible. Stay protected. Any Android. No root.*

Ghost Mode is a free, open-source personal security suite that runs silently on any Android phone through Termux. It detects threats, anonymizes your internet traffic through Tor, and monitors your device — all without rooting your phone or paying for anything.

---

## 🤔 Why Ghost Mode?

Most security tools are built for experts on laptops. Ghost Mode is different — it's built for **anyone** who wants to protect themselves on their phone. One command installs everything. One menu controls everything.

---

## 💀 What It Does

| Module | What it protects you from |
|--------|--------------------------|
| 🎙️ Mic/Camera Monitor | Apps secretly recording you |
| 🌐 Network Monitor | Suspicious outbound connections, spyware traffic |
| 👻 ARP Spoof Detector | Man-in-the-middle attacks on your WiFi |
| 🔍 Port Scanner | Exposed ports attackers can use |
| 😈 Tor Anonymity | Hides your real IP — you appear from another country |
| 🌍 Location Picker | Choose which country your traffic appears from |
| 🖥️ Browser Dashboard | Visual interface showing all scan results |
| ⏰ Auto-scan | Runs silently every 2 minutes in background |

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

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Made with 💀 for privacy.*
