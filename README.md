# 💀 Aether Ghost OS

> *Go invisible. Stay protected. Any Android. No root.*

Aether Ghost OS is a unified, sovereign privacy ecosystem designed to secure all your personal devices and networks. It runs locally and sandbox-isolated inside user-space, focusing on complete privacy and absolute digital sovereignty without requiring root access or sending your data to any cloud servers.

---

## 🤔 Why Aether Ghost OS?

Most security tools are built for experts on laptops. Aether Ghost OS is different — it's built for **anyone** who wants to protect themselves on their phone. One command installs everything. One menu controls everything.

---

---

## 🌐 Live Website

**[aetherghostos.github.io/aether-ghost-os-corp](https://aetherghostos.github.io/aether-ghost-os-corp)**

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

## 📱 Requirements

- Any Android phone (Android 6+)
- [Termux](https://f-droid.org/packages/com.termux/) installed from F-Droid
- Internet connection for setup
- **No root required**

---

## ⚡ Quick Install

Open Termux and paste this one command:

```bash
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh | bash
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

## 🧹 Cleanup, Updating & Reinstallation

If you already have a version of Aether Ghost OS running and want to perform a clean update, stop background processes, or completely remove the project, run the following commands in your Termux or Linux terminal.

### ⏹️ Step 1: Kill All Active Background Services
Running background components (like the web dashboard daemon or Tor circuits) can lock files and block package updates. Terminate them safely:
```bash
# Terminate the background web server daemon
pkill -f server_daemon.py

# Terminate active security scanner processes
pkill -f ghost_mode.py

# Stop background Tor proxy routing
pkill tor

# Stop background cron schedulers
pkill cron
```

### 🗑️ Step 2: Remove Old Project Files & Folders
Delete the old source folders, dashboard configs, and logs:
```bash
# Delete main project source folder
rm -rf ~/aether-ghost-os

# Delete dashboard web files and log registries
rm -rf ~/ghost_tools

# Delete executable scripts in your home directory
rm -f ~/ghost.sh ~/ghost_mode.py ~/setup.sh
```

### 🔄 Step 3: Run a Fresh Installation
After stopping old daemons and clearing directories, boot up the new version using the setup script:
```bash
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
```
*(Replace `AETHERGHOSTOS` with your real GitHub username).*

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
aether-ghost-os/
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

## 🛠️ Troubleshooting & Common Issues

### 1. Bot Stops Responding & Dashboard Disconnects in Background
* **Symptom:** When you leave Termux to go to WhatsApp, the dashboard shows `Scan server disconnected / Local API Offline` and your Telegram bot stops responding to `/start` or `/status` commands.
* **Cause:** Android's aggressive battery manager freezes or kills background apps (like Termux) when they are not in the foreground.
* **Solution:**
  1. **Hold a Wake Lock:** Open Termux and run `termux-wake-lock`. This tells Android to keep the CPU awake.
  2. **Disable Battery Optimization:** Go to your Android phone's **Settings ➔ Apps ➔ Termux ➔ Battery (or App Battery Usage)** and set it to **Unrestricted** (or disable "Optimize battery usage").
  3. **Use Option 11 to Exit:** If you need to exit the `ghost.sh` launcher menu to type other commands in Termux, **do not select Option 9 (Stop Everything)**. Instead, select **Option 11 (Exit Menu - Keep Services Running)**. This keeps the background dashboard daemon and Tor tunnels online.

### 2. Telegram Bot Fails to Send Alerts
* **Symptom:** Sentry alerts or tests do not appear in your Telegram chat.
* **Solution:**
  1. **Send Passcode:** Search for your bot in Telegram and start the chat by sending `/start YOUR_ADMIN_PASSCODE` (the passcode is set in `bot_config.json`, default is `CHANGE_ME_NOW`). Telegram blocks bots from sending messages to users unless the user initiates the chat first.
  2. **Verify Credentials:** Verify that your Token and Chat ID are correctly pasted on the dashboard and saved.

### 3. Too Many Server Offline Log Lines
* **Symptom:** When Termux goes to sleep, your dashboard logs are flooded with repeating warning lines.
* **Solution:** We have integrated an offline consolidated logger. The dashboard will now log exactly one warning when Termux goes offline, and one recovery message when it reconnects.

---

## ⚠️ Disclaimer

Aether Ghost OS is built for **personal security, privacy, and education only**.

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

## 🌍 Similar Tools (and why Aether Ghost OS is different)

| Tool | Root needed? | Easy setup? | Personal focus? |
|------|-------------|-------------|-----------------|
| Kali NetHunter | ✅ Yes | ❌ Complex | ❌ Offensive |
| cSploit | ✅ Yes | ❌ Complex | ❌ Offensive |
| Wireshark | ❌ No | ❌ PC only | ⚠️ Partial |
| **Aether Ghost OS** | ❌ **No** | ✅ **One command** | ✅ **Defensive** |

Aether Ghost OS is the only **no-root, one-command, defensive security suite** designed specifically for everyday Android users who want privacy and protection without being security experts.

---

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
* `/menu` — Opens the **Interactive Remote Control Dashboard** containing inline buttons to change anonymity engines, swap DNS servers, toggle DNS auto-rotation, view detailed threat reports, and run manual scans directly from Telegram.
* `/status` — Fetches current spoofed IP, active engine, anonymity health status, CPU thermalzone temperature, active DNS resolver, and threat counts.
* `/scan` — Triggers an active hardware/network security shield check instantly and returns the results.
* `/panic` — Remotely kills all Termux logs, decoys, active daemons, and disconnects all ports.

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

---

## ☕ Support & Donate

Aether Ghost OS is built and maintained independently. If this tool keeps you safe, consider supporting its development:

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

*Every contribution — no matter how small — keeps Aether Ghost OS active and secure.*

---

---

## 🔗 Connect

| Channel | Link |
|---|---|
| X / Twitter | [@AETHERGHOSTOS](https://x.com/AETHERGHOSTOS) |
| Discord | [Join Community](https://discord.gg/gNdeFA984) |
| Telegram Bot | [@AetherGhostOSbot](https://t.me/AetherGhostOSbot) |
| Telegram Group | [AetherOperatorOSCommand](https://t.me/AetherOperatorOSCommand) |
| Email | AETHERGHOSTOS@proton.me |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Made with 💀 for privacy.*
