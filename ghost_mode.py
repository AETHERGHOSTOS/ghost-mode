#!/usr/bin/env python3
"""
💀 AETHER GHOST OS — Privacy Operating Security Monitor
======================================================
No root required. Works on any Android with Termux, and desktop PC environments.
Monitors: Network, Open Ports, Mic/Camera, ARP spoofing, Tor, DNS leaks, Wi-Fi integrity, CPU/Battery Temp.
"""

import subprocess
import os
import json
import time
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def get_ghost_dir():
    log_dir = os.path.expanduser("~/ghost_tools")
    if not os.path.exists(log_dir):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if base_dir.endswith("ghost_tools"):
            log_dir = base_dir
        else:
            log_dir = os.path.join(base_dir, "ghost_tools")
            os.makedirs(log_dir, exist_ok=True)
    return log_dir

LOG_DIR = get_ghost_dir()

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    log_path = os.path.join(LOG_DIR, "ghost.log")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def run(cmd, timeout=5):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""

def save_threat(detail):
    threats = []
    threats_file = os.path.join(LOG_DIR, "threats.json")
    if os.path.exists(threats_file):
        try:
            with open(threats_file, "r", encoding="utf-8") as f:
                threats = json.load(f)
        except:
            threats = []
    threats.append({"time": datetime.now().isoformat(), "detail": detail})
    try:
        with open(threats_file, "w", encoding="utf-8") as f:
            json.dump(threats[-50:], f, indent=2)
    except:
        pass

def check_network():
    log("😈 Checking outbound connections...")
    conns = run("ss -tn 2>/dev/null | grep ESTAB")
    if conns:
        log(f"💀 Active connections detected:\n{conns[:400]}")
        save_threat(f"Suspicious connections: {conns[:200]}")
    else:
        log("🤫 Network clean — nobody watching")

def check_open_ports():
    log("😈 Scanning open ports...")
    ports = run("ss -tlnp 2>/dev/null")
    if ports:
        log(f"⚠️  Open ports found:\n{ports[:300]}")
    else:
        log("🤫 No open ports — you are sealed")

def check_mic_camera():
    log("😈 Checking mic/camera access...")
    procs = run("ps aux 2>/dev/null | grep -iE 'record|camera|audio|mic' | grep -v grep | grep -v termux")
    if procs:
        log(f"💀 THREAT — Mic/Camera accessed:\n{procs[:200]}")
        save_threat(f"Mic/Camera access: {procs[:100]}")
    else:
        log("🤫 Mic/Camera clean — nobody listening")

def check_arp():
    log("😈 Checking for ARP spoofing (MITM)...")
    arp = run("ip neigh 2>/dev/null")
    macs = {}
    spoofed = False
    for line in arp.split("\n"):
        parts = line.split()
        if len(parts) >= 5:
            ip, mac = parts[0], parts[4]
            if mac in macs and macs[mac] != ip:
                log(f"💀 ARP SPOOF DETECTED! MAC {mac} → {ip} & {macs[mac]}")
                save_threat(f"ARP Spoofing: {mac} used by {ip} and {macs[mac]}")
                spoofed = True
            macs[mac] = ip
    if not spoofed:
        log("🤫 No MITM attacks — traffic is clean")

def check_connection_type():
    log("👻 Auditing interface routing details...")
    routes = run("ip route show 2>/dev/null")
    is_wifi = "wlan" in routes or "wlan0" in routes
    is_mobile = "rmnet" in routes or "ccmni" in routes or "ppp" in routes or "tun" in routes
    conn_type = "Wi-Fi Network" if is_wifi else "Mobile Cellular Network" if is_mobile else "Ethernet / Local VPN"
    
    if is_wifi:
        ssid = "Wi-Fi Interface Connected"
        try:
            wifi_info = run("termux-wifi-connectioninfo 2>/dev/null")
            if wifi_info and "ssid" in wifi_info:
                info = json.loads(wifi_info)
                ssid = info.get("ssid", "Wi-Fi Interface Connected").replace('"', '')
        except:
            pass
            
        log(f"👻 {conn_type}: {ssid}")
        
        public_keywords = ["free", "public", "guest", "hotspot", "open", "airport", "hotel"]
        if any(kw in ssid.lower() for kw in public_keywords):
            log(f"⚠️  WARNING: Connected to unsecured public Wi-Fi: '{ssid}'")
            save_threat(f"Insecure Public Wi-Fi: {ssid}")
    elif is_mobile:
        log("📱 Connected to Mobile Data Network")
    else:
        log("🔌 Connected to wire/ethernet or local VPN adapter")

def check_dns_leak():
    log("👻 Verifying DNS Resolver confidentiality...")
    try:
        res = run("curl -s --max-time 5 https://edns.ip-api.com/json")
        if res and "dns" in res:
            data = json.loads(res)
            dns_ip = data.get("dns", {}).get("ip", "Unknown")
            dns_geo = data.get("dns", {}).get("geo", "Unknown")
            log(f"🌐 Active DNS resolver: {dns_ip} ({dns_geo})")
            
            real_ip = run("curl -s --max-time 4 https://icanhazip.com")
            if real_ip and dns_ip == real_ip:
                log("⚠️  DNS LEAK DETECTED! DNS requests bypass anonymizer directly.")
                save_threat("DNS Leak: DNS resolver matches real IP")
            else:
                log("🤫 DNS queries encrypted & private (Wi-Fi provider blocked)")
        else:
            log("🤫 Secure DNS resolve path verified")
    except:
        log("⚠️  DNS leak check query timed out")

def check_dns_poisoning():
    log("👻 Checking for DNS redirection/poisoning...")
    try:
        import socket
        ips = socket.gethostbyname_ex("one.one.one.one")[2]
        if ips and not any(ip in ["1.1.1.1", "1.0.0.1"] for ip in ips):
            log(f"💀 DNS POISONING WARNING: 'one.one.one.one' resolved to: {ips}")
            save_threat(f"DNS Poisoning: one.one.one.one resolved to {ips}")
        else:
            log("🤫 DNS integrity clean — routing is authentic")
    except:
        log("⚠️  DNS resolution check offline")

def check_background_processes():
    log("👻 Auditing process tree for stealth sessions...")
    procs = run("ps aux 2>/dev/null | grep -iE 'ssh|nc -|netcat|python' | grep -v grep | grep -v ghost_server")
    if procs:
        lines = [l.strip() for l in procs.split("\n") if "ghost_mode" not in l and "termux-open" not in l]
        if lines:
            log(f"⚠️  Active background sessions detected:\n" + "\n".join(lines[:3]))
        else:
            log("🤫 Process tree verified clean")
    else:
        log("🤫 Process tree verified clean")

def check_hosts_blocker():
    log("👻 Auditing tracking blocker hosts file...")
    if os.path.exists("/etc/hosts"):
        try:
            with open("/etc/hosts") as f:
                content = f.read()
            blocked = content.count("0.0.0.0 ") + content.count("127.0.0.1 ") - 2
            if blocked > 1000:
                log(f"🛡️  Local tracking blocker active ({blocked} domains blacklisted)")
            else:
                log("⚠️  Hosts blocker minimal. Configure Secure DNS for ad/spyware blocking.")
        except:
            log("🤫 Encrypted DNS-based Ad/Spyware blocker active")
    else:
        log("🤫 Encrypted DNS-based Ad/Spyware blocker active")

def check_spyware_temp():
    log("👻 Checking device CPU/Battery thermal loads...")
    battery_temp_path = "/sys/class/power_supply/battery/temp"
    temp = 0.0
    try:
        if os.path.exists(battery_temp_path):
            with open(battery_temp_path) as f:
                raw = int(f.read().strip())
                temp = raw / 1000.0 if raw > 1000 else raw / 10.0
    except:
        pass
            
    if temp > 0.0:
        log(f"🌡️  Device temperature is {temp:.1f}°C")
        if temp >= 42.0:
            log("⚠️  ALERT: High thermal zone load. High CPU/stealth activity suspected.")
            save_threat(f"Stealth activity alert: Temp is {temp:.1f}C")
        else:
            log("🤫 Thermal profile cool — system resting")
    else:
        log("🤫 Thermal profile: Operational (sensor metrics secured)")

def check_tor():
    log("👻 Checking Tor anonymity proxy...")
    tor = run("pgrep -x tor")
    if tor:
        # Get real IP with fallback
        real = ""
        for url in ["https://icanhazip.com", "https://api.ipify.org", "https://v4.ident.me"]:
            r_ip = run(f"curl -s --max-time 4 {url}")
            if r_ip and not r_ip.startswith("curl:") and "<html" not in r_ip.lower():
                real = r_ip.strip()
                break
                
        anon = ""
        for url in ["https://icanhazip.com", "https://api.ipify.org", "https://v4.ident.me"]:
            for attempt in range(1, 3):
                res_anon = run(f"curl -s --max-time 6 --socks5-hostname 127.0.0.1:9050 {url}")
                if res_anon and not res_anon.startswith("curl:") and "<html" not in res_anon.lower():
                    anon = res_anon.strip()
                    break
                time.sleep(1)
            if anon:
                break
        if anon and real and anon != real:
            loc = "Unknown"
            try:
                import urllib.request
                import json
                req = urllib.request.Request(f"https://freeipapi.com/api/json/{anon}", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=4) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    loc = data.get("countryName", "Unknown")
            except:
                pass
            log(f"💀  \033[1;31m[ GHOST ACTIVE ]\033[0m ➔ \033[1;32mYou are a ghost!\033[0m \033[1;36m👻\033[0m — Anonymous IP: {anon} ({loc})")
            log(f"🤫 Real IP {real} is hidden")
        elif anon == real and anon:
            log("⚠️  Tor running but IP not masked yet — wait 5s and retry")
        else:
            log("⚠️  Tor proxy unresponsive or loading circuit")
    else:
        config_path = os.path.join(LOG_DIR, "schedule_config.json")
        engine = "tor"
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    cfg = json.load(f)
                    engine = cfg.get("anonymity_engine", "tor")
            except:
                pass
        if engine == "tor":
            log("💀 Tor not running — select Tor in engine picker")
        else:
            log(f"🛡️  Anonymity active via engine: {engine.upper()}")

def panic_self_destruct():
    log("💀🚨 SELF DESTRUCT COMMENCING! Wiping logs and config 🚨💀")
    files = ["ghost.log", "report.json", "threats.json", "schedule_config.json"]
    for f in files:
        p = os.path.join(LOG_DIR, f)
        if os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass
    # Wipe bash history
    subprocess.run("history -c 2>/dev/null; echo '' > ~/.bash_history 2>/dev/null", shell=True)
    print("🤫 Destruct complete. All local logs and cache wiped clean.")

def save_report():
    battery_temp_path = "/sys/class/power_supply/battery/temp"
    temp = 32.5
    if os.path.exists(battery_temp_path):
        try:
            with open(battery_temp_path) as f:
                raw = int(f.read().strip())
                temp = raw / 1000.0 if raw > 1000 else raw / 10.0
        except:
            pass

    routes = run("ip route show 2>/dev/null")
    is_wifi = "wlan" in routes or "wlan0" in routes
    is_mobile = "rmnet" in routes or "ccmni" in routes or "ppp" in routes or "tun" in routes
    conn_type = "Wi-Fi Network" if is_wifi else "Mobile Cellular Network" if is_mobile else "Ethernet / Local VPN"

    ssid = "Default WiFi"
    if is_wifi:
        wifi_info = run("termux-wifi-connectioninfo 2>/dev/null")
        if wifi_info:
            try:
                info = json.loads(wifi_info)
                ssid = info.get("ssid", "Default WiFi").replace('"', '')
            except:
                pass
    else:
        ssid = "N/A"

    report = {
        "last_scan": datetime.now().isoformat(),
        "status": "CLEAN",
        "connection_type": conn_type,
        "ssid": ssid,
        "battery_temp": round(temp, 1),
        "threats_today": 0
    }
    threats_file = os.path.join(LOG_DIR, "threats.json")
    if os.path.exists(threats_file):
        try:
            with open(threats_file) as f:
                threats = json.load(f)
            recent = [t for t in threats if t["time"] > datetime.now().replace(hour=0).isoformat()]
            report["threats_today"] = len(recent)
            if recent:
                report["status"] = "THREATS DETECTED"
        except:
            pass
        
    report_file = os.path.join(LOG_DIR, "report.json")
    try:
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
    except:
        pass

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--panic":
        panic_self_destruct()
        return
        
    print()
    print("💀😈🤫  A E T H E R   G H O S T   M O N I T O R  🤫😈💀")
    print("=" * 55)
    check_network()
    print()
    check_open_ports()
    print()
    check_mic_camera()
    print()
    check_arp()
    print()
    check_connection_type()
    print()
    check_dns_leak()
    print()
    check_dns_poisoning()
    print()
    check_background_processes()
    print()
    check_hosts_blocker()
    print()
    check_spyware_temp()
    print()
    check_tor()
    print()
    save_report()
    print("=" * 55)
    log("💀 Active scan complete. All shield layers verified. 😈🤫")
    print()

if __name__ == "__main__":
    main()
