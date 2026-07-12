#!/usr/bin/env bash
# 💀 AETHER GHOST OS INITIALIZER & LOCKDOWN
# Runs on system boot as Root.

# ── 1. Create default live user if not exists ──────────────────────
if ! id "aether" &>/dev/null; then
    useradd -m -g users -G wheel,network,video,audio -s /bin/bash aether
    # Generate random password for the live session user
    PASS=$(openssl rand -base64 12)
    echo "aether:${PASS}" | chpasswd
    echo "wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
fi

# ── 2. Configure Firewall/iptables Network Lockdown (Tails-Style) ──
# Flush old rules
iptables -F
iptables -t nat -F

# Set default policies (Drop everything outbound/inbound by default)
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow all loopback (local) traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established/related incoming network responses
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow the Tor user (process UID) to make direct WAN connections (crucial for Tor to connect)
TOR_UID=$(id -u tor 2>/dev/null || echo "tor")
iptables -A OUTPUT -m owner --uid-owner "${TOR_UID}" -j ACCEPT

# Redirect all DNS traffic (port 53 UDP/TCP) to the Tor DNSPort (9053)
iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 9053
iptables -t nat -A OUTPUT -p tcp --dport 53 -j REDIRECT --to-ports 9053

# Block all other outbound LAN/WAN traffic to force Tor proxy routing
# Any packet trying to connect to standard ports will be dropped.

# ── 3. Start Tor Service ───────────────────────────────────────────
systemctl restart tor.service

# ── 4. Start Aether Ghost Daemon in background ──────────────────────
# The build script copies the repository to /usr/share/aether/
if [ -d "/usr/share/aether" ]; then
    cd /usr/share/aether
    python3 ghost_tools/server_daemon.py > /var/log/aether_daemon.log 2>&1 &
fi

# ── 5. Generate Desktop Shortcuts & Launchers ───────────────────────
mkdir -p /home/aether/Desktop
chown -R aether:users /home/aether

# Create Brave SOCKS5 secure wrapper in user bin
cat > /usr/local/bin/brave-secure << 'EOF'
#!/bin/bash
# Secure Brave Browser launcher for Aether Ghost OS
# Forces incognito, strict sandbox, WebRTC disable, and Tor SOCKS proxy.
exec brave-browser \
    --proxy-server="socks5://127.0.0.1:9050" \
    --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 127.0.0.1" \
    --incognito \
    --disable-webrtc \
    --disable-peer-connection-audio-api \
    --fingerprinting-canvas-image-data-noise \
    --fingerprinting-client-rects-noise \
    --no-first-run \
    "$@"
EOF
chmod +x /usr/local/bin/brave-secure

# Create Desktop launchers for Browsers
cat > /home/aether/Desktop/Tor-Browser.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Tor Browser
Comment=Anonymity exit routing
Exec=tor-browser
Icon=web-browser
Terminal=false
Categories=Network;WebBrowser;
EOF

cat > /home/aether/Desktop/Brave-Secure.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Brave Secure
Comment=Sandboxed SOCKS5 Web Browser
Exec=brave-secure
Icon=web-browser
Terminal=false
Categories=Network;WebBrowser;
EOF

cat > /home/aether/Desktop/Aether-Console.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Aether OS Console
Comment=Active Security and Sentry Control Menu
Exec=xfce4-terminal -e "python3 /usr/share/aether/ghost_mode_pc.py"
Icon=utilities-terminal
Terminal=false
Categories=System;Security;
EOF

chmod +x /home/aether/Desktop/*.desktop
chown -R aether:users /home/aether/Desktop
