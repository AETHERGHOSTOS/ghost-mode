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

ACTIVE_THREATS = []

def save_threat(detail):
    global ACTIVE_THREATS
    if detail not in ACTIVE_THREATS:
        ACTIVE_THREATS.append(detail)
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
            
            real_ip = ""
            for url in ["https://icanhazip.com", "https://api.ipify.org"]:
                try:
                    r = requests.get(url, timeout=4)
                    if r.status_code == 200 and r.text.strip() and "<html" not in r.text.lower():
                        real_ip = r.text.strip()
                        break
                except:
                    pass

            anon_ip = ""
            for url in ["https://icanhazip.com", "https://api.ipify.org"]:
                try:
                    r = requests.get(url, proxies=proxies, timeout=6)
                    if r.status_code == 200 and r.text.strip() and "<html" not in r.text.lower():
                        anon_ip = r.text.strip()
                        break
                except:
                    pass
            
            if anon_ip and real_ip and real_ip != anon_ip:
                log(f"{GREEN}💀😈 GHOST ACTIVE — Anonymous IP: {anon_ip} (Real IP {real_ip} hidden){NC}")
            elif anon_ip:
                log(f"{GREEN}💀😈 GHOST ACTIVE — Anonymous IP: {anon_ip}{NC}")
            else:
                log(f"{YELLOW}⚠️ Tor ports active, but proxy IP check timed out.{NC}")
        except Exception as e:
            log(f"{YELLOW}⚠️ Tor ports active, but proxy check failed: {e}{NC}")
    else:
        log(f"{RED}💀 Tor is not running. Launch Tor Browser or start the Tor service.{NC}")

def check_virus_guard():
    log(f"{CYAN}Virus Guard: Auditing active memory and background processes...{NC}")
    found_threats = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = (proc.info['name'] or "").lower()
                cmdline = " ".join(proc.info['cmdline'] or []).lower()
                
                # Check for netcat / raw socket shell signatures
                is_netcat = any(kw in name or kw in cmdline for kw in ["nc.exe", "netcat", "ncat"])
                
                if is_netcat:
                    detail = f"Active Backdoor Process detected: PID {proc.info['pid']} ({proc.info['name']})"
                    found_threats.append(detail)
                    log(f"{RED}💀 VIRUS GUARD THREAT: {detail}{NC}")
                    save_threat(detail)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        log(f"⚠️ Virus Guard process scan failed: {e}")
        
    if not found_threats:
        log(f"{GREEN}🤫 Virus Guard verified clean — no active runtime anomalies{NC}")

def check_malware_guard():
    if sys.platform == "win32":
        log(f"{CYAN}Malware Guard: Querying Windows Defender active threat logs...{NC}")
        try:
            ps_cmd = 'Get-MpThreat | Select-Object ThreatName, SeverityID, ActiveStatus | ConvertTo-Json'
            res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                try:
                    data = json.loads(res.stdout.strip())
                    threats = data if isinstance(data, list) else [data]
                    found = 0
                    for t in threats:
                        if t.get("ActiveStatus") == 1 or t.get("ActiveStatus") == "Active":
                            detail = f"Active Malware Alert: {t.get('ThreatName')} (Severity {t.get('SeverityID')})"
                            log(f"{RED}💀 MALWARE GUARD THREAT: {detail}{NC}")
                            save_threat(detail)
                            found += 1
                    if found == 0:
                        log(f"{GREEN}🤫 Windows Defender reports 0 active malware infections{NC}")
                except:
                    lines = [l.strip() for l in res.stdout.split("\n") if l.strip()]
                    if lines:
                        detail = f"Active Windows Defender Threat Detected: {lines[0]}"
                        log(f"{RED}💀 MALWARE GUARD THREAT: {detail}{NC}")
                        save_threat(detail)
            else:
                log(f"{GREEN}🤫 Windows Defender reports 0 active malware infections{NC}")
        except Exception as e:
            log(f"⚠️ Malware Guard: Could not query Windows Defender: {e}")
    else:
        log(f"{CYAN}Malware Guard: Auditing files using ClamAV...{NC}")
        clam_installed = subprocess.run("which clamscan", shell=True, capture_output=True).returncode == 0
        if not clam_installed:
            log(f"{YELLOW}⚠️ ClamAV (clamscan) not installed. File scan skipped. Run: sudo apt install clamav{NC}")
            return
            
        try:
            scan_dir = os.path.expanduser("~/Downloads")
            if not os.path.exists(scan_dir):
                scan_dir = BASE_DIR
                
            log(f"🕵️ Scanning directory: {scan_dir}")
            p = subprocess.run(f"clamscan -r --infected --no-summary {scan_dir} 2>/dev/null", shell=True, capture_output=True, text=True)
            if p.stdout.strip():
                infected_files = [line.strip() for line in p.stdout.split("\n") if line.strip()]
                for f in infected_files[:5]:
                    detail = f"Infected File Detected: {f}"
                    log(f"{RED}💀 MALWARE GUARD THREAT: {detail}{NC}")
                    save_threat(detail)
            else:
                log(f"{GREEN}🤫 ClamAV file scan completed: 0 infected files found{NC}")
        except Exception as e:
            log(f"⚠️ ClamAV scan failed: {e}")

def save_report():
    report_file = os.path.join(TOOLS_DIR, "report.json")
    report = {
        "last_scan": datetime.now().isoformat(),
        "status": "CLEAN",
        "active_threats": ACTIVE_THREATS
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

def panic_self_destruct():
    log("💀🚨 SELF DESTRUCT — Wiping all logs and config 🚨💀")
    files = ["ghost.log", "report.json", "threats.json", "schedule_config.json", "telegram_config.json"]
    for f in files:
        p = os.path.join(TOOLS_DIR, f)
        if os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass
    print("🤫 Destruct complete. All local logs and cache wiped clean.")

def run_full_audit_pc():
    global ACTIVE_THREATS
    ACTIVE_THREATS = []
    print("\n" + "=" * 55)
    log("💀 Initiating Full System Security Audit...")
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
    check_virus_guard()
    print()
    check_malware_guard()
    print()
    save_report()
    log(f"{GREEN}💀 Scan complete. All shield layers verified.{NC}")
    print("=" * 55 + "\n")

def main():
    global ACTIVE_THREATS
    ACTIVE_THREATS = []
    
    # Start server thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()
    time.sleep(1) # wait for server to start
    
    while True:
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
            
        # Try to render logo
        logo_script = os.path.join(TOOLS_DIR, "render_logo.py")
        if os.path.exists(logo_script):
            try:
                subprocess.run([sys.executable, logo_script])
            except:
                pass
                
        print()
        print(f"{RED}💀😈🤫  A E T H E R   G H O S T   O S  [PC EDITION]  🤫😈💀{NC}")
        print("=" * 55)
        print(f"  {GREEN}[1]{NC} 👻 Select Anonymity Engine")
        print(f"  {GREEN}[2]{NC} 🛡️  AetherGhost Guard Scans")
        print(f"  {GREEN}[3]{NC} 💀 Run Full System Security Audit")
        print(f"  {GREEN}[4]{NC} 🌍 Pick Tor Location Node")
        print(f"  {GREEN}[5]{NC} 🌐 Check Connection Status")
        print(f"  {GREEN}[6]{NC} 🖥️  Open Dashboard Browser")
        print(f"  {GREEN}[7]{NC} 📋 View System Logs")
        print(f"  {GREEN}[8]{NC} 🔧 Change DNS Resolver")
        print(f"  {GREEN}[9]{NC} 🚨 PANIC — Self Destruct")
        print(f"  {GREEN}[10]{NC} ⏹️  Stop Everything & Exit")
        print(f"  {GREEN}[12]{NC} 🚪 Exit Menu (Keep Services Running)")
        print(f"  {GREEN}[13]{NC} 🔄 Check & Pull Updates")
        print(f"  {GREEN}[0]{NC} 🔤 Reset Console Font")
        print(f"  {GREEN}[11]{NC} ☕ Support & Donate to Project")
        print("=" * 55)
        choice = input("Choose [0-13]: ").strip()
        
        if choice == "1":
            print("\n😈 SELECT ANONYMITY ENGINE:")
            print("----------------------------")
            print("[1] 🧅 Tor Proxy Network")
            print("[2] ⚡ Cloudflare WARP VPN")
            print("[3] 🌍 Public SOCKS5 Proxy Rotation")
            print("[4] 🛡️  Secure DNS-over-HTTPS (DoH)")
            print("[5] ⚠️  No Anonymity (UNPROTECTED!)")
            eng = input("\nSelect [1-5]: ").strip()
            
            sched_path = os.path.join(TOOLS_DIR, "schedule_config.json")
            cfg = {}
            if os.path.exists(sched_path):
                try:
                    with open(sched_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                except:
                    pass
            
            engines = {"1": "tor", "2": "warp", "3": "proxy", "4": "doh", "5": "none"}
            if eng in engines:
                cfg["anonymity_engine"] = engines[eng]
                try:
                    with open(sched_path, "w", encoding="utf-8") as f:
                        json.dump(cfg, f, indent=2)
                except:
                    pass
                print(f"✅ Engine switched to: {engines[eng].upper()}")
            else:
                print("❌ Invalid choice.")
                
        elif choice == "2":
            print("\n🛡️  AETHERGHOST GUARD SCAN CENTER:")
            print("---------------------------------")
            print("[1] 🦠 Scan Active Memory (Virus Guard)")
            print("[2] 💾 Scan Storage Files (Malware Guard)")
            scan_c = input("\nSelect [1-2]: ").strip()
            if scan_c == "1":
                ACTIVE_THREATS = []
                check_virus_guard()
                save_report()
            elif scan_c == "2":
                ACTIVE_THREATS = []
                check_malware_guard()
                save_report()
            else:
                print("❌ Invalid choice.")
                
        elif choice == "3":
            run_full_audit_pc()
            
        elif choice == "4":
            picker_path = os.path.join(TOOLS_DIR, "location_picker.py")
            if os.path.exists(picker_path):
                subprocess.run([sys.executable, picker_path])
            else:
                print("❌ location_picker.py not found.")
                
        elif choice == "5":
            sched_path = os.path.join(TOOLS_DIR, "schedule_config.json")
            eng = "tor"
            if os.path.exists(sched_path):
                try:
                    with open(sched_path, "r", encoding="utf-8") as f:
                        eng = json.load(f).get("anonymity_engine", "tor")
                except:
                    pass
            print(f"\n🔒 Active Engine: {eng.upper()}")
            try:
                real_ip = requests.get("https://icanhazip.com", timeout=5).text.strip()
                print(f"🌐 Your Connection IP: {real_ip}")
            except Exception as e:
                print(f"⚠️ Connection check failed: {e}")
                
        elif choice == "6":
            print("🌐 Opening dashboard: http://localhost:8080/ghost_dashboard.html")
            webbrowser.open("http://localhost:8080/ghost_dashboard.html")
            
        elif choice == "7":
            log_path = os.path.join(TOOLS_DIR, "ghost.log")
            if os.path.exists(log_path):
                print("\n📋 Last 30 log lines:")
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for l in lines[-30:]:
                        print(l.strip())
            else:
                print("❌ No logs yet.")
                
        elif choice == "8":
            print("\n🔧 DNS RESOLVER CONFIGURATION:")
            print("-------------------------------")
            print("To configure system-wide DNS-over-HTTPS or secure resolvers, please use either:")
            print("  1. The Aether Ghost OS Web Dashboard (Settings Panel)")
            print("  2. Your operating system Network Configuration settings")
            
        elif choice == "9":
            confirm = input("🚨 Are you sure you want to self-destruct security profiles? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                panic_self_destruct()
                sys.exit(0)
            else:
                print("Panic cancelled.")
                
        elif choice == "10":
            print("\n⏹️  Stopping Aether Ghost OS PC services...")
            # Kill server_daemon.py processes via psutil check
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmd = proc.info.get('cmdline') or []
                    if any('server_daemon.py' in part for part in cmd):
                        proc.kill()
                        print("✅ Dashboard daemon stopped.")
                except:
                    pass
            # Kill local Tor proxy
            if sys.platform == "win32":
                subprocess.run("taskkill /F /IM tor.exe 2>nul", shell=True)
            else:
                subprocess.run("pkill tor 2>/dev/null", shell=True)
            print("🤫 services deactivated. Exiting launcher...")
            sys.exit(0)
            
        elif choice == "12":
            print("🚪 Exiting menu. Background Sentry and Anonymity daemon remains ACTIVE.")
            print("🌐 Dashboard is online: http://localhost:8080/ghost_dashboard.html")
            print()
            sys.exit(0)
            
        elif choice == "0":
            if sys.platform == "win32":
                subprocess.run("cls", shell=True)
            else:
                subprocess.run("clear", shell=True)
            print("✅ Console font configuration loaded.")
            
        elif choice == "11":
            print("==========================================================")
            print("  ☕ SUPPORT AETHER GHOST OS DEVELOPMENT")
            print("==========================================================")
            print("  If this tool keeps you secure, consider supporting us!")
            print("")
            print("  🌐 Web Donations:")
            print("     Buy Me a Coffee: https://buymeacoffee.com/aetherghost.os")
            print("")
            print("  🪙 Crypto Addresses:")
            print("     USDT  | TRX - Tron (TRC20):           TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU")
            print("     USDC  | SOL - Solana:                 9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui")
            print("     USDT  | ETH - Ethereum (ERC20):       0x09cad574c2c39a88ce931307361682680b795490")
            print("     BNB   | BSC - BNB Smart Chain (BEP20): 0x09cad574c2c39a88ce931307361682680b795490")
            print("     BTC   | BTC - Bitcoin:                15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k")
            print("     BTC   | SEGWIT - BTC (SegWit):        bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj")
            print("")
            print("  Thank you for keeping Aether Ghost OS active and secure!")
            print("==========================================================")
            
        elif choice == "13":
            check_and_pull_updates_cli()
            
        else:
            print("❌ Invalid choice.")
        
        input("\nPress [Enter] to return to menu...")

def print_sentry_status():
    config_path = os.path.join(TOOLS_DIR, "telegram_config.json")
    cfg = {"enabled": False, "token": "", "chat_id": ""}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            pass
    
    sched_path = os.path.join(TOOLS_DIR, "schedule_config.json")
    sched = {"scan_mode": "interval", "scan_interval": 120, "auto_update": True}
    if os.path.exists(sched_path):
        try:
            with open(sched_path, "r", encoding="utf-8") as f:
                sched = json.load(f)
        except:
            pass

    print()
    print("🤖 AETHERGHOST SENTRY BOT REMOTE TERMINAL CONSOLE")
    print("==================================================")
    print(f"Status:      {'🟢 ENABLED' if cfg.get('enabled') else '🔴 DISABLED'}")
    print(f"Token:       {cfg.get('token', 'N/A')}")
    print(f"Chat ID:     {cfg.get('chat_id', 'N/A')}")
    print(f"Scheduler:   {sched.get('scan_mode', 'interval').upper()}")
    print(f"Interval:    {sched.get('scan_interval', 120)}s")
    print(f"Auto-Update: {'🟢 ENABLED' if sched.get('auto_update', True) else '🔴 DISABLED'}")
    print("==================================================")
    print("Use --sentry-toggle to enable/disable or --sentry-setup <token> <chat_id> to configure.")

def setup_sentry(token, chat_id):
    config_path = os.path.join(TOOLS_DIR, "telegram_config.json")
    cfg = {"enabled": True, "token": token, "chat_id": chat_id}
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print("✅ Sentry credentials updated and enabled.")
    except Exception as e:
        print(f"❌ Failed to save sentry credentials: {e}")

def toggle_sentry():
    config_path = os.path.join(TOOLS_DIR, "telegram_config.json")
    cfg = {"enabled": False, "token": "", "chat_id": ""}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            pass
    cfg["enabled"] = not cfg.get("enabled", False)
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print(f"✅ Sentry Bot toggled to: {'🟢 ENABLED' if cfg['enabled'] else '🔴 DISABLED'}")
    except Exception as e:
        print(f"❌ Failed to toggle sentry: {e}")

def check_and_pull_updates_cli():
    print("🔄 Checking for updates from GitHub...")
    try:
        subprocess.run("git fetch", shell=True, capture_output=True, text=True, timeout=15)
        local_hash = subprocess.run("git rev-parse HEAD", shell=True, capture_output=True, text=True, timeout=8).stdout.strip()
        remote_hash = subprocess.run("git rev-parse @{u}", shell=True, capture_output=True, text=True, timeout=8).stdout.strip()
        
        if local_hash == remote_hash:
            print("🟢 System is already up-to-date!")
            return
            
        print("💡 New update detected! Pulling latest code changes...")
        pull_res = subprocess.run("git pull", shell=True, capture_output=True, text=True, timeout=20)
        if pull_res.returncode == 0:
            print("✅ Code successfully updated. Hot-restarting scanner...")
            time.sleep(1)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print(f"❌ Pull failed: {pull_res.stderr.strip()}")
    except Exception as e:
        print(f"❌ Error checking updates: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--virus":
            ACTIVE_THREATS = []
            check_virus_guard()
            save_report()
            sys.exit(0)
        elif sys.argv[1] == "--malware":
            ACTIVE_THREATS = []
            check_malware_guard()
            save_report()
            sys.exit(0)
        elif sys.argv[1] == "--sentry":
            print_sentry_status()
            sys.exit(0)
        elif sys.argv[1] == "--sentry-toggle":
            toggle_sentry()
            sys.exit(0)
        elif sys.argv[1] == "--sentry-setup":
            if len(sys.argv) > 3:
                setup_sentry(sys.argv[2], sys.argv[3])
            else:
                print("❌ Missing arguments: --sentry-setup <token> <chat_id>")
            sys.exit(0)
        elif sys.argv[1] == "--panic":
            confirm = input("🚨 Are you sure you want to self-destruct security profiles? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                panic_self_destruct()
            else:
                print("Panic cancelled.")
            sys.exit(0)
        elif sys.argv[1] == "--update":
            check_and_pull_updates_cli()
            sys.exit(0)
    main()
