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

## 💻 Supported Environments

* **Android**: Any phone running Android 6+ (No root required)
* **Linux**: Ubuntu, Debian, Fedora, Arch Linux, and CentOS
* **macOS**: Apple Silicon or Intel architecture (with Homebrew)
* **Windows**: Windows 10/11 running WSL (Windows Subsystem for Linux)

---

## ⚡ Installation & Quick Start

### 🤖 Option 1: Android (via Termux)

#### Step 1: Install Termux on your phone
> [!WARNING]
> Do **NOT** install Termux from the Google Play Store. The Play Store version is deprecated and cannot update packages.

* **If F-Droid is working:** Download the [Termux app directly on F-Droid](https://f-droid.org/packages/com.termux/).
* **If F-Droid is down or failing to download:**
  1. Go to the official **[Termux GitHub Releases](https://github.com/termux/termux-app/releases)**.
  2. Scroll to the latest release assets and download the `.apk` file (typically labeled `universal` or `arm64-v8a`).
  3. Install the downloaded APK file manually on your phone.

#### Step 2: Install Ghost Mode
Open Termux and run the universal setup installer:
```bash
curl -sL https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main/setup.sh | bash
```

---

### 🐧 Option 2: Linux (Ubuntu, Debian, Arch)

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

### 🍏 Option 3: macOS

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

### 🪟 Option 4: Windows (WSL)

1. Open PowerShell as Administrator and enable Windows Subsystem for Linux (if not already installed):
   ```powershell
   wsl --install
   ```
2. Open your newly installed Linux terminal environment (e.g., Ubuntu for Windows) and follow the **Option 2: Linux** guide above!


## 🚀 Usage

After install, run:

```bash
bash ~/ghost.sh
```

You'll see this menu:

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
