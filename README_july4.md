# ≡ƒÆÇ Aether Ghost OS

> *Go invisible. Stay protected. Any Android. No root.*

Aether Ghost OS is a unified, sovereign privacy ecosystem designed to secure all your personal devices and networks. It runs locally and sandbox-isolated inside user-space, focusing on complete privacy and absolute digital sovereignty without requiring root access or sending your data to any cloud servers.

---

## ≡ƒñö Why Aether Ghost OS?

Most security tools are built for experts on laptops. Aether Ghost OS is different ΓÇö it's built for **anyone** who wants to protect themselves on their phone. One command installs everything. One menu controls everything.

---

---

## ≡ƒîÉ Live Website

**[aetherghostos.github.io/aether-ghost-os-corp](https://aetherghostos.github.io/aether-ghost-os-corp)**

---


## ≡ƒÆÇ Core Modules

| Module | What it protects you from |
|--------|--------------------------|
| **≡ƒÄÖ∩╕Å Privacy Sentry** | Monitors Android camera and microphone log access in real-time, preventing spy apps from recording you. |
| **≡ƒ¢í∩╕Å Deception Sentry** | Traps and delays unauthorized network scans on port `2222` with a decoy SSH tarpit honeypot, reporting intrusions instantly. |
| **≡ƒîÉ Sovereign Tor Routing** | Routes Termux web requests and scans securely through Tor, utilizing country-rotational SOCKS5 proxy circuits. |
| **≡ƒÆ¼ Scam Sentry** | Offline-compatible link and message scanner running inside Telegram to check incoming SMS for fraud, phishing, and bad links. |
| **≡ƒöä Failover Daemon** | Background loop that tests connection health and automatically rotates between Tor, Cloudflare WARP, and secure DNS. |
| **≡ƒûÑ∩╕Å Browser Dashboard** | Interactive local console showing all hardware scan results, speed tests, and log streams. |
| **ΓÅ░ Auto-scan** | Lightweight loop that runs silently every 2 minutes in the background, consuming minimal battery. |

---

## ≡ƒô▒ Requirements

- Any Android phone (Android 6+)
- [Termux](https://f-droid.org/packages/com.termux/) installed from F-Droid
- Internet connection for setup
- **No root required**

---

## ΓÜí Quick Install

Open Termux and paste this one command:

```bash
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh | bash
```

That's it. Everything installs automatically.

---

## ≡ƒÜÇ Usage

After install, run:

```bash
bash ~/ghost.sh
```

You'll see this menu:

```
  ≡ƒÆÇ≡ƒÿê≡ƒñ½  G H O S T   M O D E  ≡ƒñ½≡ƒÿê≡ƒÆÇ
  ========================================
  Personal Security Suite for Android

  [1] ≡ƒÆÇ Run Security Scan
  [2] ≡ƒÿê Go Anonymous (Tor)
  [3] ≡ƒîì Pick My Location
  [4] ≡ƒîÉ Check My IP
  [5] ≡ƒûÑ∩╕Å  Open Dashboard
  [6] ≡ƒôï View Logs
  [7] ΓÅ╣∩╕Å  Stop Everything
```

---

## ≡ƒº╣ Cleanup, Updating & Reinstallation

If you already have a version of Aether Ghost OS running and want to perform a clean update, stop background processes, or completely remove the project, run the following commands in your Termux or Linux terminal.

### ΓÅ╣∩╕Å Step 1: Kill All Active Background Services
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

### ≡ƒùæ∩╕Å Step 2: Remove Old Project Files & Folders
Delete the old source folders, dashboard configs, and logs:
```bash
# Delete main project source folder
rm -rf ~/aether-ghost-os

# Delete dashboard web files and log registries
rm -rf ~/ghost_tools

# Delete executable scripts in your home directory
rm -f ~/ghost.sh ~/ghost_mode.py ~/setup.sh
```

### ≡ƒöä Step 3: Run a Fresh Installation
After stopping old daemons and clearing directories, boot up the new version using the setup script:
```bash
curl -sL https://raw.githubusercontent.com/AETHERGHOSTOS/ghost-mode/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
```
*(Replace `AETHERGHOSTOS` with your real GitHub username).*

---

## ≡ƒîì Location Picker

Ghost Mode lets you choose which country your internet traffic appears to come from:

```
  [1]  ≡ƒç║≡ƒç╕ United States
  [2]  ≡ƒç¼≡ƒçº United Kingdom
  [3]  ≡ƒç⌐≡ƒç¬ Germany
  [4]  ≡ƒç│≡ƒç▒ Netherlands
  ...and 16 more countries
  [0]  ≡ƒîì Random (auto)
```

Pick one or multiple countries. Your traffic rotates through them automatically.

---

## ≡ƒôü Project Structure

```
aether-ghost-os/
Γö£ΓöÇΓöÇ ghost_mode.py          # Main security scanner
Γö£ΓöÇΓöÇ ghost.sh               # Launcher menu
Γö£ΓöÇΓöÇ setup.sh               # Universal installer
Γö£ΓöÇΓöÇ ghost_tools/
Γöé   Γö£ΓöÇΓöÇ location_picker.py # Tor country picker
Γöé   ΓööΓöÇΓöÇ ghost_dashboard.html # Browser dashboard
Γö£ΓöÇΓöÇ assets/
Γöé   ΓööΓöÇΓöÇ logo.svg           # Ghost Mode logo
ΓööΓöÇΓöÇ README.md
```

---

## Γ¥ô Common Questions

**Does it work offline?**
Core scanning (network, mic/camera, ARP, ports) works fully offline. Tor anonymity requires internet.

**Will it drain my battery?**
Ghost Mode is lightweight. The scan runs in under 5 seconds every 2 minutes and uses minimal resources.

**Can websites detect Tor?**
Some sites (Netflix, banking apps) block known Tor IPs. For regular browsing and anonymity, Tor works well. Pair with Surfshark VPN for better results.

**Does my location change automatically?**
Yes ΓÇö every time you restart Tor or start a new session, you get a different IP. You can also manually pick a location using option 3.

**Can it prevent attacks?**
Ghost Mode detects threats and alerts you. It hides your real IP from attackers. It does not replace a full firewall but provides strong personal protection for everyday use.

---

## ΓÜá∩╕Å Disclaimer

Aether Ghost OS is built for **personal security, privacy, and education only**.

- Γ£à Protect your own device and network
- Γ£à Learn about cybersecurity
- Γ£à Monitor your own traffic
- Γ¥î Do not use against others without permission
- Γ¥î Do not use for illegal activities

The developer takes no responsibility for misuse.

---

## ≡ƒ¢á∩╕Å Built With

- Python 3
- Bash
- Tor
- Nmap
- Termux API
- HTML/CSS/JS (dashboard)

---

## ≡ƒîì Similar Tools (and why Aether Ghost OS is different)

| Tool | Root needed? | Easy setup? | Personal focus? |
|------|-------------|-------------|-----------------|
| Kali NetHunter | Γ£à Yes | Γ¥î Complex | Γ¥î Offensive |
| cSploit | Γ£à Yes | Γ¥î Complex | Γ¥î Offensive |
| Wireshark | Γ¥î No | Γ¥î PC only | ΓÜá∩╕Å Partial |
| **Aether Ghost OS** | Γ¥î **No** | Γ£à **One command** | Γ£à **Defensive** |

Aether Ghost OS is the only **no-root, one-command, defensive security suite** designed specifically for everyday Android users who want privacy and protection without being security experts.

---

---

## ≡ƒñû Optional: Telegram Sentry & Scam Detection Bot

Aether Ghost OS includes a companion Telegram Bot system that sends real-time push alerts to your phone and lets you audit your device remotely or analyze incoming scam messages.

### ≡ƒîƒ Bot Capabilities & Scenarios

| Trigger / Action | Bot Response | Risk Assessment / Result |
|---|---|---|
| **≡ƒÜ¿ Intrusion Detection** | Real-time push notification | `"≡ƒÜ¿ Intrusion Alert! Decoy Honeypot port scan detected from IP 192.168.1.15."` |
| **≡ƒÜ¿ Security Threat** | Threat Alert | `"ΓÜá∩╕Å Threat Alert! Microphones currently in use by background process: SpywareAgent"` |
| **≡ƒöä Failover Routing** | Status Alert | `"≡ƒöä Anonymity Pivot: Tor tunnel connection lost. Failover engine WARP connect succeeded."` |
| **≡ƒÆ¼ Forwarded Phishing link** | Domain Risk Analysis | **≡ƒö┤ HIGH RISK:** `"Γ¥î paypa1-verification.xyz ΓÇö Lookalike domain spoofing PayPal with high-risk TLD."` |
| **≡ƒÆ¼ Forwarded SMS scam text** | Text Keyword Audit | **≡ƒö┤ HIGH RISK:** `"Urgency/Fraud Language Detected (lottery winner, m-pesa reference code)."` |
| **≡ƒÆ¼ Forwarded Safe message** | Domain Verification | **≡ƒƒó LOW RISK:** `"Γ£à safaricom.co.ke ΓÇö Recognized domain. No scam indicators detected."` |

### ≡ƒò╣∩╕Å Remote Bot Commands (Send to your private bot chat)
* `/menu` ΓÇö Opens the **Interactive Remote Control Dashboard** containing inline buttons to change anonymity engines, swap DNS servers, toggle DNS auto-rotation, view detailed threat reports, and run manual scans directly from Telegram.
* `/status` ΓÇö Fetches current spoofed IP, active engine, anonymity health status, CPU thermalzone temperature, active DNS resolver, and threat counts.
* `/scan` ΓÇö Triggers an active hardware/network security shield check instantly and returns the results.
* `/panic` ΓÇö Remotely kills all Termux logs, decoys, active daemons, and disconnects all ports.

### ≡ƒôí Automatic Background Scan Alerts
The Sentry Bot will automatically send an alert message to your Telegram chat after *every* scheduled background scan completes (runs every 2 minutes):
* **Clean Scan:** Sends a confirmation confirming all systems are secure and anonymity layers are holding (e.g. `All Systems Secure (0 threats found). Anonymity layers holding. ≡ƒæ╗`).
* **Threat Detected:** Sends a warning showing how many threats were detected, with a recommendation to check the visual dashboard or send `/menu` to audit the issues.

---

### ΓÜÖ∩╕Å Step-by-Step Setup Guide

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

## Γÿò Support & Donate

Aether Ghost OS is built and maintained independently. If this tool keeps you safe, consider supporting its development:

### ≡ƒîÉ Web Donations
| Platform | Link |
|---|---|
| Γÿò Buy Me a Coffee | [buymeacoffee.com/aetherghost.os](https://buymeacoffee.com/aetherghost.os) |

### ≡ƒ¬Ö Crypto
| Token | Network | Address |
|---|---|---|
| USDT | TRX ΓÇö Tron (TRC20) | `TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU` |
| USDC | SOL ΓÇö Solana | `9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui` |
| USDT | ETH ΓÇö Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| BNB | BSC ΓÇö BNB Smart Chain (BEP20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| BNB | ETH ΓÇö Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | BTC ΓÇö Bitcoin | `15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k` |
| Bitcoin | BSC ΓÇö BNB Smart Chain (BEP20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | ETH ΓÇö Ethereum (ERC20) | `0x09cad574c2c39a88ce931307361682680b795490` |
| Bitcoin | SEGWIT ΓÇö BTC (SegWit) | `bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj` |

*Every contribution ΓÇö no matter how small ΓÇö keeps Aether Ghost OS active and secure.*

---

---

## ≡ƒöù Connect

| Channel | Link |
|---|---|
| X / Twitter | [@AETHERGHOSTOS](https://x.com/AETHERGHOSTOS) |
| Discord | [Join Community](https://discord.gg/gNdeFA984) |
| Telegram Bot | [@AetherGhostOSbot](https://t.me/AetherGhostOSbot) |
| Telegram Group | [AetherOperatorOSCommand](https://t.me/AetherOperatorOSCommand) |
| Email | AETHERGHOSTOS@proton.me |

---

## ≡ƒôä License

MIT License ΓÇö free to use, modify, and distribute.

---

*Made with ≡ƒÆÇ for privacy.*
