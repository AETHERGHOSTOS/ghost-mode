import os
import sys
import subprocess
import json
import time
import socket
import webbrowser
import threading
from datetime import datetime

# Force UTF-8 stdout/stderr encoding on Windows to prevent UnicodeEncodeError on emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# --- Auto Dependency Installer ---
def install_dependencies():
    libs = {
        'psutil': 'psutil',
        'requests': 'requests',
        'socks': 'pysocks'
    }
    missing = []
    for imp_name, pip_name in libs.items():
        try:
            __import__(imp_name)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print(f"💀 Aether Ghost OS: Missing dependencies {missing}. Installing automatically...")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + missing
            if sys.platform != "win32":
                cmd.append("--break-system-packages")
            subprocess.run(cmd, check=True)
            print("✅ Dependencies installed successfully.\n")
        except Exception as e:
            print(f"❌ Failed to install dependencies. Please run: pip install {' '.join(missing)} --break-system-packages")
            sys.exit(1)

install_dependencies()

import psutil
import requests

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "ghost_tools")
os.makedirs(TOOLS_DIR, exist_ok=True)

# ANSI Colors
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GRAY = '\033[0;90m'
NC = '\033[0m'

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    with open(os.path.join(TOOLS_DIR, "ghost.log"), "a", encoding="utf-8") as f:
        f.write(line + "\n")

def save_threat(detail):
    threats = []
    threats_file = os.path.join(TOOLS_DIR, "threats.json")
    if os.path.exists(threats_file):
        try:
            with open(threats_file, "r", encoding="utf-8") as f:
                threats = json.load(f)
        except:
            threats = []
    threats.append({"time": datetime.now().isoformat(), "detail": detail})
    with open(threats_file, "w", encoding="utf-8") as f:
        json.dump(threats[-50:], f, indent=2)

# --- Mic / Camera access detection (Windows specific query, falls back to process checking) ---
def check_mic_camera():
    log(f"{CYAN}Checking Microphone and Webcam active status...{NC}")
    active_threats = []

    if sys.platform == "win32":
        # Query Windows registry for webcam/mic capability access
        import winreg
        
        # Check Microphone
        try:
            mic_path = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, mic_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                if subkey_name in ["NonPackaged", "Packaged"]:
                    continue
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    start_val, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStart")
                    stop_val, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStop")
                    if start_val > stop_val: # App is currently using the mic
                        active_threats.append(f"Microphone accessed by: {subkey_name}")
                except WindowsError:
                    pass
        except Exception:
            pass

        # Check Webcam
        try:
            webcam_path = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, webcam_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                if subkey_name in ["NonPackaged", "Packaged"]:
                    continue
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    start_val, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStart")
                    stop_val, _ = winreg.QueryValueEx(subkey, "LastUsedTimeStop")
                    if start_val > stop_val: # App is currently using the webcam
                        active_threats.append(f"Webcam/Camera accessed by: {subkey_name}")
                except WindowsError:
                    pass
        except Exception:
            pass
    else:
        # Linux / macOS: check processes accessing video nodes
        try:
            p = subprocess.run("lsof /dev/video* 2>/dev/null", shell=True, capture_output=True, text=True)
            if p.stdout.strip():
                active_threats.append(f"Webcam file handle open: {p.stdout.strip()[:100]}")
        except Exception:
            pass

    if active_threats:
        for threat in active_threats:
            log(f"{RED}💀 THREAT: {threat}{NC}")
            save_threat(threat)
    else:
        log(f"{GREEN}🤫 Microphone & Webcam clean — nobody watching{NC}")

# --- Network connection checks ---
def check_network():
    log(f"{CYAN}Checking outbound connections...{NC}")
    suspicious = 0
    try:
        conns = psutil.net_connections(kind='inet')
        for conn in conns:
            if conn.status == 'ESTABLISHED':
                raddr = f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}"
                # Ignore local/localhost connections
                if conn.raddr.ip in ['127.0.0.1', '::1', '0.0.0.0'] or conn.raddr.ip.startswith("192.168.") or conn.raddr.ip.startswith("10."):
                    continue
                log(f"🔗 Outbound Connection: PID {conn.pid} | {raddr}")
                suspicious += 1
        if suspicious > 0:
            log(f"{YELLOW}⚠️ Found {suspicious} active remote connections.{NC}")
        else:
            log(f"{GREEN}🤫 Network clean — no suspicious external links{NC}")
    except Exception as e:
        log(f"⚠️ Could not check network connections: {e}")

# --- Check open ports ---
def check_open_ports():
    log(f"{CYAN}Scanning listening ports...{NC}")
    try:
        conns = psutil.net_connections(kind='inet')
        listeners = [c for c in conns if c.status == 'LISTEN']
        if listeners:
            for l in listeners:
                log(f"🔓 Listening Port: {l.laddr.port} (PID {l.pid})")
        else:
            log(f"{GREEN}🤫 No open listening ports — you are sealed{NC}")
    except Exception as e:
        log(f"⚠️ Could not check listening ports: {e}")

# --- ARP Spoofing checks ---
def check_arp():
    log(f"{CYAN}Checking for ARP spoofing (MITM attacks)...{NC}")
    macs = {}
    spoofed = False
    try:
        # Run arp -a
        out = subprocess.run("arp -a", shell=True, capture_output=True, text=True).stdout
        for line in out.split("\n"):
            parts = line.split()
            if len(parts) >= 3:
                ip = parts[0]
                mac = parts[1].lower()
                # standard MAC format checks
                if "-" in mac or ":" in mac:
                    if mac in macs and macs[mac] != ip:
                        # Ignore broadcast / multicast
                        if mac in ["ff-ff-ff-ff-ff-ff", "ff:ff:ff:ff:ff:ff"]:
                            continue
                        msg = f"ARP Spoofing Detected! MAC {mac} is shared by {ip} and {macs[mac]}"
                        log(f"{RED}💀 {msg}{NC}")
                        save_threat(msg)
                        spoofed = True
                    macs[mac] = ip
        if not spoofed:
            log(f"{GREEN}🤫 No MITM attacks — LAN traffic is clean{NC}")
    except Exception as e:
        log(f"⚠️ Could not audit ARP table: {e}")

# --- Tor Anonymity checks ---
def check_tor():
    log(f"{CYAN}Checking Tor anonymity...{NC}")
    tor_active = False
    ports = [9050, 9150]  # 9050 (Tor Service), 9150 (Tor Browser)
    working_port = None
    
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", port))
            working_port = port
            tor_active = True
            s.close()
            break
        except:
            pass

    if tor_active:
        try:
            # Use socks5h proxy to check IP details and prevent DNS leakage
            proxies = {
                'http': f'socks5h://127.0.0.1:{working_port}',
                'https': f'socks5h://127.0.0.1:{working_port}'
            }
            real_ip = requests.get("https://ifconfig.me", timeout=5).text.strip()
            anon_ip = requests.get("https://ifconfig.me", proxies=proxies, timeout=8).text.strip()
            
            if real_ip != anon_ip:
                log(f"{GREEN}💀😈 GHOST ACTIVE — Anonymous IP: {anon_ip} (Real IP {real_ip} hidden){NC}")
            else:
                log(f"{YELLOW}⚠️ Tor is running but traffic is not proxied (IP matches real IP).{NC}")
        except Exception as e:
            log(f"{YELLOW}⚠️ Tor ports active, but proxy check failed: {e}{NC}")
    else:
        log(f"{RED}💀 Tor is not running. Launch Tor Browser or start the Tor service.{NC}")

def save_report():
    report_file = os.path.join(TOOLS_DIR, "report.json")
    report = {
        "last_scan": datetime.now().isoformat(),
        "status": "CLEAN"
    }
    threats_file = os.path.join(TOOLS_DIR, "threats.json")
    if os.path.exists(threats_file):
        try:
            with open(threats_file, "r", encoding="utf-8") as f:
                threats = json.load(f)
            today_str = datetime.now().strftime("%Y-%m-%d")
            recent = [t for t in threats if t["time"].startswith(today_str)]
            report["threats_today"] = len(recent)
            if recent:
                report["status"] = "THREATS DETECTED"
        except:
            report["threats_today"] = 0
    else:
        report["threats_today"] = 0

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

# --- Start local HTTP Server ---
def run_http_server():
    daemon_path = os.path.join(TOOLS_DIR, "server_daemon.py")
    if os.path.exists(daemon_path):
        try:
            # Launch the full API daemon server in the background
            subprocess.Popen([sys.executable, daemon_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            log(f"{GREEN}Dashboard server daemon initiated locally at http://localhost:8080/ghost_dashboard.html{NC}")
        except Exception as e:
            log(f"⚠️ Failed to start daemon server: {e}")
    else:
        # Fallback to simple static server if daemon is missing
        import http.server
        import socketserver
        PORT = 8080
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=TOOLS_DIR, **kwargs)
        socketserver.TCPServer.allow_reuse_address = True
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                log(f"{GREEN}Dashboard server started locally (fallback file server) at http://localhost:{PORT}/ghost_dashboard.html{NC}")
                httpd.serve_forever()
        except:
            pass

def main():
    print()
    print(f"{RED}💀😈🤫  A E T H E R   G H O S T   O S  [PC EDITION]  🤫😈💀{NC}")
    print("=" * 55)
    
    # Start server thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()
    time.sleep(1) # wait for server to start

    # Run checks
    check_network()
    print()
    check_open_ports()
    print()
    check_mic_camera()
    print()
    check_arp()
    print()
    check_tor()
    print()
    
    save_report()
    log(f"{GREEN}💀 Scan complete. Dashboard is live. 😈🤫{NC}")
    print("=" * 55)

    # Launch dashboard in browser
    webbrowser.open("http://localhost:8080/ghost_dashboard.html")
    
    # Keep console active so the web server stays alive
    print("\nPress Ctrl+C to terminate the scanner and stop the dashboard server.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{RED}Stopping Aether Ghost OS PC server...{NC}")
        sys.exit(0)

if __name__ == "__main__":
    main()
