# 💀 Aether Ghost OS — Master Project Specification
**Author:** Project Administrator / Owner  
**Release Version:** v1.1.2  
**Target Audience:** Development Team / Contributors  

---

## 1. Project Overview & Objective
**Aether Ghost OS** is an open-source, user-space privacy and security environment designed to run locally on mobile devices (via Termux on Android) and personal computers. It secures outbound connection routing, logs unauthorized local hardware access, traps local network scans using honeypot decoys, and alerts users via a personal Telegram Sentry.

---

## 2. System Architecture & Components
The ecosystem contains four core files:

| File | Language | Role | Description |
|---|---|---|---|
| `ghost_mode.py` | Python | **Threat Scanner** | Modular scanner checking connection types, open ports, mic/camera access logs, ARP table spoofing, DNS integrity, and CPU load. |
| `server_daemon.py` | Python | **Background Server** | Light server running on port `8080` that serves the UI, runs scheduled scans, handles failovers, and operates Sentry Bot. |
| `ghost_dashboard.html` | HTML/CSS/JS | **Visual Panel** | Responsive cyber-console visualizer for settings, logs, threat telemetry, and security checks. |
| `support_bot.py` | Python | **Support Operator** | Standard customer-facing 2-way support messaging bot mapping anonymous inquiries directly to the admin chat. |

---

## 3. Issues Fixed in the Current Milestone
The following bugs have been fully fixed and merged into `main`:

1. **Broken Logo URL (Case-Sensitivity Bug):** 
   - *Problem:* The dashboard showed a broken image icon for the main logo because it requested `logo.png` instead of the capitalized `LOGO.png` hosted on GitHub.
   - *Fix:* Aligned case-sensitivity across `setup.sh` and fallback URLs in `ghost_dashboard.html`.
2. **Standard Termux Whitelisting (False Alarms):**
   - *Problem:* Normal background processes like `ssh-agent`, `runsv`, `sshd`, and `pulseaudio` were flagged as spyware threats by the scanner.
   - *Fix:* Whitelisted these normal system dependencies in `ghost_mode.py`.
3. **Passcode Plaintext Leak (CodeQL Alert):**
   - *Problem:* The support bot printed the raw admin passcode in plaintext to the console terminal during startup.
   - *Fix:* Masked the printed passcode logs in `support_bot.py`.
4. **Sentry Bot Poller Timeout Freezes:**
   - *Problem:* Poller froze trying to run blocking network audits live when requested `/status` or `/menu`.
   - *Fix:* Updated the poller to reply using cached connection statuses instantly.

---

## 4. Active Backlog & Issues for the Dev Team
The following tasks are assigned to the development team to build and resolve:

### Task A: Log File Size Rotation (Backend / Python)
* **Description:** The server logs all terminal actions to `ghost.log` inside `~/ghost_tools/`. Currently, this file grows indefinitely and will consume device storage.
* **Goal:** Implement a file rotation handler inside `server_daemon.py` to limit log file size to 2MB, saving up to 3 backup logs.

### Task B: Custom Process Whitelist Editor (Automation / UI)
* **Description:** Users currently have to modify python code to add whitelisted processes.
* **Goal:** Create a JSON config (`whitelist.json`) where users can add safe app names (e.g. `pulseaudio`). Update `ghost_mode.py` to load this dynamically.

### Task C: Mock Offline Testing Framework (Quality Assurance / Python)
* **Description:** Running tests requires active connections and hardware, which makes debugging difficult in offline environments.
* **Goal:** Write unit tests using pytest and mock modules to simulate various network states (Tor active, inactive, DNS poisoning).
