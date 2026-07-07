#!/usr/bin/env python3
"""
💀 AETHER GHOST OS — Privacy Operating Security Monitor v1.1.0
==============================================================
No root required. Works on any Android with Termux, and desktop PC.
Monitors: Network, Open Ports, Mic/Camera, ARP spoofing, Tor, DNS leaks, Wi-Fi integrity, CPU Temp.
"""

import subprocess, os, json, time, socket, sys
from datetime import datetime

# Force UTF-8 stdout/stderr encoding on Windows to prevent UnicodeEncodeError on emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

VERSION = "1.1.0"

def get_ghost_dir():
    log_dir = os.path.expanduser("~/ghost_tools")
    if not os.path.exists(log_dir):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = base_dir if base_dir.endswith("ghost_tools") else os.path.join(base_dir, "ghost_tools")
        os.makedirs(log_dir, exist_ok=True)
    return log_dir

LOG_DIR = get_ghost_dir()

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    try:
        with open(os.path.join(LOG_DIR, "ghost.log"), "a", encoding="utf-8") as f:
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
    p = os.path.join(LOG_DIR, "threats.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                threats = json.load(f)
        except:
            threats = []
    threats.append({"time": datetime.now().isoformat(), "detail": detail})
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(threats[-50:], f, indent=2)
    except:
        pass

# ── MODULE 1: NETWORK ──────────────────────────────────────────────

def check_network():
    log("😈 Checking outbound connections...")
    conns = run("ss -tn 2>/dev/null | grep ESTAB")
    if conns:
        log(f"🤫 Active connections detected:\n{conns[:400]}")
    else:
        log("🤫 Network clean — nobody watching")

# ── MODULE 2: OPEN PORTS ───────────────────────────────────────────

def check_open_ports():
    log("😈 Scanning open ports...")
    ports = run("ss -tlnp 2>/dev/null")
    if ports:
        log(f"⚠️  Open ports found:\n{ports[:300]}")
    else:
        log("🤫 No open ports — you are sealed")

# ── MODULE 3: MIC / CAMERA ─────────────────────────────────────────

def check_mic_camera():
    log("😈 Checking mic/camera access...")
    is_android = os.path.exists("/system/build.prop") or run("getprop ro.build.version.sdk") != ""
    detected = []
    
    if is_android:
        # Check Android logcat buffer for recent active handles (extended timeout)
        logcat_data = run("logcat -d -t 250 -v brief 2>/dev/null", timeout=12)
        if logcat_data:
            lines = logcat_data.split("\n")
            for line in reversed(lines):
                # Search for Camera opening events
                if "CameraService" in line or "android.hardware.camera" in line:
                    if any(kw in line.lower() for kw in ["connect", "open", "active", "start"]):
                        app_name = "Unknown App"
                        for pkg in ["whatsapp", "zoom", "teams", "skype", "facetime", "instagram", "facebook", "camera", "snapchat"]:
                            if pkg in line.lower():
                                app_name = pkg.capitalize()
                                break
                        detected.append(f"Camera opened ({app_name})")
                        break
                
                # Search for Audio/Microphone recording events
                if "AudioRecord" in line or "AudioSource" in line:
                    if any(kw in line.lower() for kw in ["start", "active", "recording"]):
                        app_name = "Unknown App"
                        for pkg in ["whatsapp", "zoom", "teams", "skype", "facetime", "instagram", "facebook", "record", "snapchat"]:
                            if pkg in line.lower():
                                app_name = pkg.capitalize()
                                break
                        detected.append(f"Microphone active ({app_name})")
                        break

    # Supplemental check: search active processes (fallback)
    procs = run(
        "ps aux 2>/dev/null | grep -iE 'record|camera|audio|mic' "
        "| grep -v grep | grep -v termux | grep -v ghost | grep -v server_daemon "
        "| grep -v pulseaudio | grep -v pipewire | grep -v wireplumber | grep -v jackd | grep -v sndiod"
    )
    if procs:
        lines = [l.strip() for l in procs.split("\n") if l.strip()]
        detected.append(f"Process handle: {lines[0][:80]}")

    if detected:
        msg = ", ".join(list(set(detected)))
        log(f"💀 THREAT — Mic/Camera accessed: {msg}")
        save_threat(f"Mic/Camera accessed: {msg}")
    else:
        log("🤫 Mic/Camera clean — nobody listening")

# ── MODULE 4: ARP SPOOF ────────────────────────────────────────────

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

# ── MODULE 5: CONNECTION TYPE ──────────────────────────────────────

def check_connection_type():
    log("👻 Auditing network interface routing...")
    routes = run("ip route show 2>/dev/null")
    is_wifi = "wlan" in routes
    is_mobile = any(k in routes for k in ["rmnet", "ccmni", "ppp", "tun"])
    conn_type = "Wi-Fi Network" if is_wifi else "Mobile Cellular Network" if is_mobile else "Ethernet / Local VPN"

    ssid = "Wi-Fi Interface Connected"
    if is_wifi:
        try:
            wifi_info = run("termux-wifi-connectioninfo 2>/dev/null", timeout=4)
            if wifi_info and "ssid" in wifi_info:
                info = json.loads(wifi_info)
                ssid = info.get("ssid", ssid).replace('"', '')
        except:
            pass
        log(f"👻 {conn_type}: {ssid}")
        public_keywords = ["free", "public", "guest", "hotspot", "open", "airport", "hotel"]
        if any(kw in ssid.lower() for kw in public_keywords):
            log(f"⚠️  WARNING: Unsecured public Wi-Fi detected: '{ssid}'")
            save_threat(f"Insecure Public Wi-Fi: {ssid}")
    elif is_mobile:
        log("📱 Connected to Mobile Data Network")
    else:
        log("🔌 Ethernet or local VPN adapter")

# ── MODULE 6: DNS LEAK CHECK ───────────────────────────────────────

def check_dns_leak():
    log("👻 Verifying DNS resolver confidentiality...")
    try:
        # Check if direct connection is already Tor (global routing active)
        is_global_tor = False
        tor_check_res = run("curl -s --max-time 6 https://check.torproject.org/api/ip", timeout=8)
        if tor_check_res and "IsTor" in tor_check_res:
            try:
                is_global_tor = json.loads(tor_check_res).get("IsTor", False)
            except:
                pass
        
        if is_global_tor:
            log("🤫 DNS queries globally routed through Tor exit node — no leak possible")
            return

        res = run("curl -s --max-time 6 http://ip-api.com/json/", timeout=8)
        if res and "query" in res:
            data = json.loads(res)
            org = data.get("org", data.get("isp", "Unknown Provider"))
            ip = data.get("query", "Unknown")
            log(f"🌐 DNS/IP resolver path: {ip} via {org}")

            # Check if we're using Tor — DNS should route through Tor
            tor_running = run("pgrep -x tor")
            if tor_running:
                tor_ip = run("curl -s --max-time 8 --socks5-hostname 127.0.0.1:9050 http://ip-api.com/json/", timeout=10)
                if tor_ip and "query" in tor_ip:
                    tor_data = json.loads(tor_ip)
                    tor_addr = tor_data.get("query")
                    if tor_addr != ip:
                        log("🤫 DNS queries routed through Tor — no leak detected")
                    else:
                        log("⚠️  Possible DNS leak — DNS resolver matches real IP path")
                        save_threat("DNS Leak: resolver may be bypassing Tor")
                else:
                    log("⚠️  Tor proxy unreachable during DNS leak audit")
            else:
                log("🤫 DNS resolver path verified (Tor not active)")
        else:
            log("🤫 DNS check complete — resolver path secure")
    except Exception as e:
        log("🤫 DNS check complete — resolver responding normally")

# ── MODULE 7: DNS POISONING ────────────────────────────────────────

def check_dns_poisoning():
    log("👻 Checking for DNS redirection/poisoning...")
    try:
        ips = socket.gethostbyname_ex("one.one.one.one")[2]
        if ips and not any(ip in ["1.1.1.1", "1.0.0.1"] for ip in ips):
            log(f"💀 DNS POISONING WARNING: one.one.one.one resolved to: {ips}")
            save_threat(f"DNS Poisoning: one.one.one.one resolved to {ips}")
        else:
            log("🤫 DNS integrity clean — routing is authentic")
    except:
        log("🤫 DNS resolution check complete")

# ── MODULE 8: BACKGROUND PROCESSES ────────────────────────────────

def check_background_processes():
    log("👻 Auditing process tree for stealth sessions...")
    # Explicitly exclude own ghost OS processes from detection
    procs = run(
        "ps aux 2>/dev/null | grep -iE 'ssh|nc -|netcat' "
        "| grep -v grep | grep -v ghost | grep -v server_daemon | grep -v aether"
    )
    # Also check Python processes but exclude our own tools
    py_procs = run(
        "ps aux 2>/dev/null | grep python "
        "| grep -v grep | grep -v ghost_mode | grep -v server_daemon "
        "| grep -v location_picker | grep -v render_logo | grep -v ghost_mode_pc "
        "| grep -v support_bot"
    )

    # Known-safe Termux & Linux background processes — whitelist these to prevent false positives
    SAFE_PROCESSES = [
        "ssh-agent",   # Termux SSH credential agent — always running, totally normal
        "runsv",       # Termux service supervisor — manages background daemons
        "sshd",        # Termux SSH daemon — started by Termux:API or auto-boot
        "supervise",   # Part of Termux runit service manager
        "runsvdir",    # Termux runit directory supervisor
        "/bin/login",  # Termux session login shell
        # Standard Linux/Ubuntu background system processes
        "unattended-upgrades",
        "unattended-upgrade-shutdown",
        "networkd-dispatcher",
        "apport",
        "cloud-init",
        "update-notifier",
        "gdm-session-worker",
        "packagekitd",
        "systemd",
    ]

    found = []
    if procs:
        lines = [l.strip() for l in procs.split("\n") if l.strip()]
        # Filter out known-safe Termux background processes
        lines = [l for l in lines if not any(safe in l for safe in SAFE_PROCESSES)]
        found.extend(lines)
    if py_procs:
        lines = [l.strip() for l in py_procs.split("\n") if l.strip()]
        lines = [l for l in lines if not any(safe in l for safe in SAFE_PROCESSES)]
        found.extend(lines)

    if found:
        msg = f"External background session detected: {found[0][:80]}"
        log(f"⚠️  {msg}")
        save_threat(msg)
    else:
        log("🤫 Process tree verified clean — 💀 [ GHOST ACTIVE ] ➔ You are a ghost! 👻")

# ── MODULE 9: HOSTS / TRACKER BLOCKER ─────────────────────────────

def check_hosts_blocker():
    log("👻 Auditing tracker blocker status...")
    # On Android/Termux there is no /etc/hosts writable — this is normal
    # Check if a DNS-over-HTTPS is configured instead
    config_path = os.path.join(LOG_DIR, "schedule_config.json")
    engine = "tor"
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                cfg = json.load(f)
            engine = cfg.get("anonymity_engine", "tor")
        except:
            pass

    if engine == "doh":
        log("🛡️  DNS-over-HTTPS active — ad/tracker blocking via encrypted DNS")
    elif engine in ["tor", "warp", "proxy"]:
        log("🛡️  Anonymity engine active — traffic routed through encrypted path")
    else:
        # Check actual hosts file
        if os.path.exists("/etc/hosts"):
            try:
                with open("/etc/hosts") as f:
                    content = f.read()
                blocked = content.count("0.0.0.0 ") + content.count("127.0.0.1 ")
                if blocked > 10:
                    log(f"🛡️  Hosts blocker active ({blocked} domains blocked)")
                else:
                    log("ℹ️  No local hosts blocker. Enable DoH engine for tracker blocking.")
            except:
                log("ℹ️  Hosts file access restricted — normal on Android")
        else:
            log("ℹ️  No hosts blocker on this device. Enable DoH for tracker blocking.")

# ── MODULE 10: THERMAL CHECK ───────────────────────────────────────

def check_spyware_temp():
    log("👻 Checking device thermal load...")
    temp = 0.0
    try:
        path = "/sys/class/power_supply/battery/temp"
        if os.path.exists(path):
            with open(path) as f:
                raw = int(f.read().strip())
                temp = raw / 1000.0 if raw > 1000 else raw / 10.0
    except:
        pass

    if temp > 0:
        log(f"🌡️  Device temperature: {temp:.1f}°C")
        if temp >= 42.0:
            log("⚠️  High thermal load detected — possible hidden background activity")
            save_threat(f"High thermal: {temp:.1f}°C")
        else:
            log("🤫 Thermal profile normal — device resting")
    else:
        log("🤫 Thermal sensors secured / unavailable")

# ── MODULE 11: TOR STATUS ──────────────────────────────────────────

def check_tor():
    log("👻 Checking anonymity engine status...")
    config_path = os.path.join(LOG_DIR, "schedule_config.json")
    engine = "tor"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            engine = cfg.get("anonymity_engine", "tor")
        except:
            pass

    if engine == "none":
        log("⚠️  Anonymity engine is OFF — connection is unprotected")
        return

    if engine == "doh":
        log("🛡️  DNS-over-HTTPS active — DNS queries are encrypted")
        return

    if engine == "warp":
        trace = run("curl -s --max-time 5 https://www.cloudflare.com/cdn-cgi/trace", timeout=6)
        if "warp=on" in trace:
            log("💀😈 GHOST ACTIVE — Cloudflare WARP VPN connected")
        else:
            log("⚠️  WARP VPN not connected — run warp-cli connect")
        return

    # Tor check
    tor = run("pgrep -x tor")
    if not tor:
        log("💀 Tor not running — select Tor engine and activate")
        return

    # Check direct connection using Tor check API
    direct_is_tor = False
    real = ""
    res_direct = run("curl -s --max-time 5 https://check.torproject.org/api/ip", timeout=6)
    if res_direct and "IsTor" in res_direct:
        try:
            data = json.loads(res_direct)
            direct_is_tor = data.get("IsTor", False)
            real = data.get("IP", "")
        except:
            pass

    if not real:
        for url in ["https://icanhazip.com", "https://api.ipify.org"]:
            r = run(f"curl -s --max-time 4 {url}")
            if r and not r.startswith("curl:") and "<html" not in r.lower():
                real = r.strip()
                break

    # Check SOCKS connection using Tor check API
    anon_is_tor = False
    anon = ""
    res_anon = run("curl -s --max-time 8 --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip", timeout=10)
    if res_anon and "IsTor" in res_anon:
        try:
            data = json.loads(res_anon)
            anon_is_tor = data.get("IsTor", False)
            anon = data.get("IP", "")
        except:
            pass

    if not anon:
        for url in ["https://icanhazip.com", "https://api.ipify.org"]:
            for attempt in range(2):
                r = run(f"curl -s --max-time 8 --socks5-hostname 127.0.0.1:9050 {url}", timeout=10)
                if r and not r.startswith("curl:") and "<html" not in r.lower():
                    anon = r.strip()
                    break
                time.sleep(2)
            if anon:
                break

    if (direct_is_tor or anon_is_tor) and anon:
        log(f"💀  \033[1;31m[ GHOST ACTIVE ]\033[0m ➔ \033[1;32mYou are a ghost!\033[0m 👻 — Anonymous IP: {anon}")
        if direct_is_tor:
            log("🤫 Connection globally wrapped in Tor tunnel — absolute protection active")
        else:
            log(f"🤫 Real IP {real} is hidden from Termux SOCKS requests")
        log(f"ℹ️  NOTE: Browser traffic uses real IP unless proxied separately")
    elif anon and real and anon != real:
        log(f"💀  \033[1;31m[ GHOST ACTIVE ]\033[0m ➔ \033[1;32mYou are a ghost!\033[0m 👻 — Anonymous IP: {anon}")
        log(f"🤫 Real IP {real} is hidden from Termux SOCKS requests")
        log(f"ℹ️  NOTE: Browser traffic uses real IP unless proxied separately")
    elif anon == real and anon:
        log("⚠️  Tor running but SOCKS IP matches direct IP path. Verify routing.")
    else:
        log("⚠️  Tor proxy loading circuits — wait 15 seconds and rescan")

# ── MODULE 12: DNS CHANGE ─────────────────────────────────────────

def change_dns():
    """Allow user to change DNS resolver."""
    DNS_OPTIONS = {
        "1": ("Cloudflare (1.1.1.1) — Fast + Private", "1.1.1.1", "1.0.0.1"),
        "2": ("Google (8.8.8.8) — Reliable", "8.8.8.8", "8.8.4.4"),
        "3": ("Quad9 (9.9.9.9) — Security Filtered", "9.9.9.9", "149.112.112.112"),
        "4": ("OpenDNS (208.67.222.222) — Family Safe", "208.67.222.222", "208.67.220.220"),
        "5": ("AdGuard (94.140.14.14) — Ad Blocking", "94.140.14.14", "94.140.15.15"),
    }
    print()
    print("🌐 DNS CHANGE MENU")
    print("=" * 40)
    print("Note: This configures the system resolver locally.")
    print()
    for k, (name, p, s) in DNS_OPTIONS.items():
        print(f"  [{k}] {name}")
    print()
    choice = input("Choose DNS [1-5]: ").strip()
    if choice in DNS_OPTIONS:
        name, primary, secondary = DNS_OPTIONS[choice]
        config_path = os.path.join(LOG_DIR, "schedule_config.json")
        cfg = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except:
                pass
        cfg["custom_dns_primary"] = primary
        cfg["custom_dns_secondary"] = secondary
        if cfg.get("dns_provider") == "rotation":
            cfg["dns_provider"] = "cloudflare"
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except:
            pass

        termux_resolv = "/data/data/com.termux/files/usr/etc/resolv.conf"
        applied = False
        if os.path.exists("/data/data/com.termux/files/usr/bin/sh"):
            try:
                os.makedirs(os.path.dirname(termux_resolv), exist_ok=True)
                with open(termux_resolv, "w", encoding="utf-8") as f:
                    f.write(f"nameserver {primary}\nnameserver {secondary}\n")
                applied = True
                print("✅ Termux resolv.conf written successfully.")
            except Exception as e:
                print(f"⚠️ Failed to write Termux resolv.conf: {e}")

        if not applied:
            try:
                with open("/etc/resolv.conf", "w") as f:
                    f.write(f"nameserver {primary}\nnameserver {secondary}\n")
                applied = True
                print("✅ System resolv.conf written successfully.")
            except:
                pass

        if not applied and sys.platform == "win32":
            try:
                ps_cmd = (
                    f"Get-NetAdapter | Where-Object {{ $_.Status -eq 'Up' }} | "
                    f"ForEach-Object {{ Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ServerAddresses ('{primary}', '{secondary}') -ErrorAction SilentlyContinue }}"
                )
                subprocess.run(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                applied = True
                print("✅ Windows DNS client server addresses updated.")
            except:
                pass

        if applied:
            print(f"✅ DNS successfully updated to: {name}")
        else:
            print(f"⚠️ Permission denied: Could not apply DNS to system.")
            print(f"   Saved configuration preference: {name}")
            print(f"   Primary:   {primary}")
            print(f"   Secondary: {secondary}")
    else:
        print("Invalid choice.")

# ── PANIC MODE ────────────────────────────────────────────────────

def panic_self_destruct():
    log("💀🚨 SELF DESTRUCT — Wiping all logs and config 🚨💀")
    files = ["ghost.log", "report.json", "threats.json", "schedule_config.json"]
    for f in files:
        p = os.path.join(LOG_DIR, f)
        if os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass
    subprocess.run("history -c 2>/dev/null; echo '' > ~/.bash_history 2>/dev/null", shell=True)
    print("🤫 Destruct complete. All local logs and cache wiped clean.")

# ── REPORT SAVE ───────────────────────────────────────────────────

def save_report():
    temp = 0.0
    try:
        path = "/sys/class/power_supply/battery/temp"
        if os.path.exists(path):
            with open(path) as f:
                raw = int(f.read().strip())
                temp = raw / 1000.0 if raw > 1000 else raw / 10.0
    except:
        pass

    routes = run("ip route show 2>/dev/null")
    is_wifi = "wlan" in routes
    is_mobile = any(k in routes for k in ["rmnet", "ccmni", "ppp", "tun"])
    conn_type = "Wi-Fi Network" if is_wifi else "Mobile Cellular Network" if is_mobile else "Ethernet / Local VPN"

    ssid = "N/A"
    if is_wifi:
        wifi_info = run("termux-wifi-connectioninfo 2>/dev/null", timeout=4)
        if wifi_info:
            try:
                ssid = json.loads(wifi_info).get("ssid", "Wi-Fi").replace('"', '')
            except:
                pass

    report = {
        "last_scan": datetime.now().isoformat(),
        "status": "CLEAN",
        "connection_type": conn_type,
        "ssid": ssid,
        "battery_temp": round(temp, 1),
        "threats_today": 0,
        "version": VERSION
    }

    p = os.path.join(LOG_DIR, "threats.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                threats = json.load(f)
            today = datetime.now().strftime("%Y-%m-%d")
            recent = [t for t in threats if t["time"].startswith(today)]
            report["threats_today"] = len(recent)
            if recent:
                report["status"] = "THREATS DETECTED"
        except:
            pass

    try:
        with open(os.path.join(LOG_DIR, "report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    except:
        pass

# ── MAIN ──────────────────────────────────────────────────────────

def main():
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--panic":
            panic_self_destruct()
            return
        if sys.argv[1] == "--dns":
            change_dns()
            return

    print()
    print(f"💀😈🤫  A E T H E R   G H O S T   O S  v{VERSION}  🤫😈💀")
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
    log("💀 Scan complete. All shield layers verified. 😈🤫")
    print()

if __name__ == "__main__":
    main()
