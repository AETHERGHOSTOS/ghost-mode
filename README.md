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

## 📱 Requirements

- Any Android phone (Android 6+)
- [Termux](https://f-droid.org/packages/com.termux/) installed from F-Droid
- Internet connection for setup
- **No root required**

---

## ⚡ Quick Install

Open Termux and paste this one command:

```bash
curl -sL https://raw.githubusercontent.com/YOURUSERNAME/ghost-mode/main/setup.sh | bash
```

That's it. Everything installs automatically.

---

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
