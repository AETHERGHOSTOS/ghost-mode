# Aether Ghost OS — Linux Installation Guide (Kali, Parrot, Ubuntu)

Run Aether Ghost OS on Kali Linux, Parrot OS, or any Debian-based distribution.

## 🛠️ Step 1: Install Dependencies
Open your terminal and run:
```bash
sudo apt update
sudo apt install -y python3 python3-pip nmap net-tools curl tor iptables
```

## 📦 Step 2: Clone and Configure
Clone your private repository (assuming you have access):
```bash
git clone https://github.com/YOURUSERNAME/aether-ghost-os.git
cd aether-ghost-os
chmod +x setup.sh
```

## 👻 Step 3: Run the Monitor
Run the local scanner:
```bash
python3 ghost_mode_pc.py
```
This will automatically launch the dashboard server at `http://localhost:8080/ghost_dashboard.html` and open it in your default web browser.

## 🛡️ Step 4: Active Honeypot Blocking
To enable automatic IP blocking when hackers scan your port 2222, launch Aether Ghost OS with root/sudo permissions:
```bash
sudo python3 ghost_mode_pc.py
```
If an intruder is caught scanning, the system will instantly apply an `iptables` drop rule to secure your machine.
