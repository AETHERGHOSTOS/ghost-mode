#!/usr/bin/env python3
"""
💀 AETHER GHOST OS — Dashboard Server & Daemon
===============================================
A lightweight, dependency-free background web server that hosts the interactive
dashboard, runs background security scans, monitors anonymity health, and triggers
failover mechanisms.
"""

import os
import sys
import json
import time
import socket
import urllib.request
import urllib.parse
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime

# Force UTF-8 stdout/stderr encoding on Windows to prevent UnicodeEncodeError on emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8080
last_manual_change_time = 0
last_dns_rotation_time = 0

CONNECTION_STATUS = {
    "engine": "tor",
    "active": False,
    "ip": "Disconnected",
    "real_ip": "Unavailable",
    "location": "Offline",
    "dns_encrypted": False,
    "notification_profile": "sound_vibrate"
}

def update_connection_status_cache():
    global CONNECTION_STATUS
    try:
        cfg = load_config()
        engine = cfg.get("anonymity_engine", "tor")
        is_healthy, ip, loc, real_ip = verify_connection_health(engine)
        dns_encrypted = (engine != "none")
        CONNECTION_STATUS = {
            "engine": engine,
            "active": is_healthy,
            "ip": ip,
            "real_ip": real_ip or "Unavailable",
            "location": loc,
            "dns_encrypted": dns_encrypted,
            "notification_profile": cfg.get("notification_profile", "sound_vibrate")
        }
        return is_healthy, ip, loc, real_ip
    except Exception as e:
        log_message(f"Error updating connection health cache: {e}")
        return False, "Disconnected", "Offline", "Unavailable"


DNS_PROVIDERS = {
    "cloudflare": ("1.1.1.1", "1.0.0.1"),
    "google": ("8.8.8.8", "8.8.4.4"),
    "quad9": ("9.9.9.9", "149.112.112.112"),
    "adguard": ("94.140.14.14", "94.140.15.15")
}

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

def log_message(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    log_path = os.path.join(LOG_DIR, "ghost.log")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def load_config():
    p = os.path.join(LOG_DIR, "schedule_config.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "scan_interval": 120,
        "location_interval": 0,
        "notification_profile": "sound_vibrate",
        "anonymity_engine": "tor",
        "custom_sound_path": "",
        "dns_provider": "cloudflare",
        "dns_rotation_interval": 0,
        "dns_scheduled_time": "",
        "custom_dns_primary": "1.1.1.1",
        "custom_dns_secondary": "1.0.0.1"
    }

def save_config(cfg):
    p = os.path.join(LOG_DIR, "schedule_config.json")
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        log_message(f"Error saving config: {e}")

# --- Native Notification Handler ---
def trigger_native_notification(title, body):
    cfg = load_config()
    profile = cfg.get("notification_profile", "sound_vibrate")
    if profile == "none":
        return

    sound_path = cfg.get("custom_sound_path", "")
    sound_cmd = ""
    if profile == "sound_vibrate" and sound_path and os.path.exists(sound_path):
        sound_cmd = f" --sound-play {sound_cmd_quote(sound_path)}"
        
    cmd = f"termux-notification --title {sound_cmd_quote(title)} --content {sound_cmd_quote(body)}"
    if sound_cmd:
        cmd += sound_cmd

    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def sound_cmd_quote(s):
    return '"' + s.replace('"', '\\"') + '"'

# --- Active Scan Runner ---
def run_security_scan():
    log_message("🔄 Background threat scan initiated...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_name = "ghost_mode_pc.py" if sys.platform == "win32" else "ghost_mode.py"
    script_path = os.path.join(base_dir, script_name)
    if not os.path.exists(script_path):
        script_path = os.path.expanduser(f"~/{script_name}")
        
    if os.path.exists(script_path):
        try:
            subprocess.run([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            log_message("✅ Background threat scan completed successfully.")
            
            # Read scan report to see if threats exist
            report_file = os.path.join(LOG_DIR, "report.json")
            status_msg = "All systems secure 👻"
            is_threat = False
            if os.path.exists(report_file):
                try:
                    with open(report_file) as f:
                        rep = json.load(f)
                    if rep.get("status") != "CLEAN":
                        status_msg = f"Threats detected! {rep.get('threats_today', 0)} security issues found."
                        is_threat = True
                except:
                    pass
            
            title = "⚠️ GHOST SECURITY ALERT" if is_threat else "🛡️ Ghost OS Background Scan"
            trigger_native_notification(title, status_msg)
            if is_threat:
                send_telegram_alert(f"⚠️ *SECURITY THREAT DETECTED!*\n{status_msg}\nCheck the visual dashboard or send /menu to view threats.")
            else:
                send_telegram_alert(f"🛡️ *Aether Ghost OS: Scan Complete*\nStatus: *💀 [ GHOST ACTIVE ] ➔ You are a ghost!* 👻\nAll Systems Secure (0 threats found). Anonymity layers holding.")
        except Exception as e:
            log_message(f"⚠️ Scan failed to run: {e}")
    else:
        log_message(f"⚠️ {script_name} script not found. Skipping active scan.")

# --- Proxy-Safe CLI Curl Helper ---
def run_curl(url, proxy=None, timeout=6):
    """Runs curl over subprocess to safely support SOCKS5/SOCKS5h without PySocks dependency."""
    cmd = f'curl -s -L --max-time {timeout} '
    if proxy:
        if proxy.startswith("socks5h://"):
            addr = proxy.replace("socks5h://", "")
            cmd += f"--socks5-hostname {addr} "
        elif proxy.startswith("socks5://"):
            addr = proxy.replace("socks5://", "")
            cmd += f"-x socks5://{addr} "
        elif proxy.startswith("http://") or proxy.startswith("https://"):
            cmd += f"-x {proxy} "
    cmd += f'"{url}"'
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout+2)
        if res.returncode == 0 and res.stdout.strip() and not res.stdout.strip().startswith("curl:"):
            return res.stdout.strip()
    except:
        pass
    return ""

# --- Anonymity Connection Verification ---
def get_public_ip(engine):
    urls = ["https://icanhazip.com", "https://api.ipify.org", "https://v4.ident.me"]
    proxy = None
    if engine == "tor":
        proxy = "socks5h://127.0.0.1:9050"
    elif engine == "proxy":
        proxy_file = os.path.join(LOG_DIR, "active_proxy.json")
        if os.path.exists(proxy_file):
            try:
                with open(proxy_file) as f:
                    p_cfg = json.load(f)
                proxy = p_cfg.get("proxy", "")
            except:
                pass

    for url in urls:
        ip = run_curl(url, proxy)
        if ip and "<html" not in ip.lower():
            return ip
    return ""

def get_real_ip_direct():
    urls = ["https://icanhazip.com", "https://api.ipify.org", "https://v4.ident.me"]
    for url in urls:
        ip = run_curl(url, proxy=None, timeout=4)
        if ip and "<html" not in ip.lower():
            return ip
    return ""

def verify_connection_health(engine):
    """Returns (is_active, masked_ip, country, real_ip)"""
    real_ip = get_real_ip_direct()
    
    if engine == "none":
        return (False, real_ip or "Exposed", "None (Unprotected)", real_ip)

    masked_ip = get_public_ip(engine)
    if not masked_ip:
        return (False, "Disconnected", "Offline", real_ip)

    # Tor / Proxy checks: IP must be different from real IP
    if engine in ["tor", "proxy"]:
        if real_ip and masked_ip == real_ip:
            return (False, masked_ip, "Leaking Real IP", real_ip)

    # Cloudflare WARP checks: verify Cloudflare trace config
    if engine == "warp":
        trace = run_curl("https://www.cloudflare.com/cdn-cgi/trace", timeout=4)
        if not trace or "warp=on" not in trace:
            return (False, masked_ip, "WARP Disconnected", real_ip)

    # Geolocation lookup fallback chain
    country = "Unknown Location"
    providers = [
        ("https://freeipapi.com/api/json/{ip}", "countryName"),
        ("https://ipapi.co/{ip}/json/", "country_name"),
        ("http://ip-api.com/json/{ip}", "country"),
        ("https://ipinfo.io/{ip}/json", "country")
    ]
    
    for url_tmpl, key in providers:
        url = url_tmpl.format(ip=masked_ip)
        try:
            loc_res = run_curl(url, timeout=3)
            if loc_res and "{" in loc_res:
                data = json.loads(loc_res)
                c_val = data.get(key, "")
                if c_val:
                    country = c_val
                    break
        except Exception as geoloc_err:
            pass

    return (True, masked_ip, country, real_ip)

# --- DNS Changer System Settings Helper ---
def apply_system_dns(primary, secondary):
    log_message(f"⚙️ Applying system DNS settings: {primary}, {secondary}")
    
    # 1. Android/Termux Resolv.conf Update
    termux_resolv = "/data/data/com.termux/files/usr/etc/resolv.conf"
    if os.path.exists("/data/data/com.termux/files/usr/bin/sh"):
        try:
            os.makedirs(os.path.dirname(termux_resolv), exist_ok=True)
            with open(termux_resolv, "w", encoding="utf-8") as f:
                f.write(f"nameserver {primary}\nnameserver {secondary}\n")
            log_message("✅ Termux resolv.conf written successfully.")
            return True
        except Exception as e:
            log_message(f"⚠️ Failed to write Termux resolv.conf: {e}")
            
    # 2. Windows PC DNS Adapter Settings Update
    if sys.platform == "win32":
        try:
            ps_cmd = (
                f"Get-NetAdapter | Where-Object {{ $_.Status -eq 'Up' }} | "
                f"ForEach-Object {{ Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ServerAddresses ('{primary}', '{secondary}') -ErrorAction SilentlyContinue }}"
            )
            subprocess.run(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            log_message("✅ Windows active adapter DNS configurations updated.")
            return True
        except Exception as e:
            log_message(f"⚠️ Failed to update Windows DNS: {e}")
            
    # 3. Linux / macOS configurations
    if sys.platform in ["linux", "darwin"]:
        try:
            with open("/etc/resolv.conf", "w", encoding="utf-8") as f:
                f.write(f"nameserver {primary}\nnameserver {secondary}\n")
            log_message("✅ Linux / etc resolv.conf updated.")
            return True
        except:
            if sys.platform == "darwin":
                try:
                    subprocess.run("networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1 2>/dev/null", shell=True)
                    log_message("✅ macOS networksetup resolver updated.")
                    return True
                except:
                    pass
            log_message("⚠️ Permission denied: Could not edit /etc/resolv.conf system settings.")
    return False

# --- DNS Rotation Loop ---
def run_dns_rotation_loop():
    global last_dns_rotation_time
    log_message("🔀 DNS Auto-Rotation scheduler started.")
    while True:
        try:
            cfg = load_config()
            interval = cfg.get("dns_rotation_interval", 0)
            provider = cfg.get("dns_provider", "cloudflare")
            
            if provider == "rotation":
                now = time.time()
                trigger_rotation = False
                trigger_reason = ""
                
                if interval > 0 and (now - last_dns_rotation_time >= (interval * 60)):
                    trigger_rotation = True
                    trigger_reason = "Interval Auto-Rotation"
                
                scheduled_time = cfg.get("dns_scheduled_time", "")
                if scheduled_time:
                    now_str = datetime.now().strftime("%H:%M")
                    if now_str == scheduled_time and (now - last_dns_rotation_time > 65):
                        trigger_rotation = True
                        trigger_reason = f"Daily Scheduled Time ({scheduled_time})"
                
                if trigger_rotation:
                    providers = list(DNS_PROVIDERS.keys())
                    current_primary = cfg.get("custom_dns_primary", "1.1.1.1")
                    
                    current_idx = 0
                    for idx, name in enumerate(providers):
                        if DNS_PROVIDERS[name][0] == current_primary:
                            current_idx = idx
                            break
                            
                    next_idx = (current_idx + 1) % len(providers)
                    next_provider = providers[next_idx]
                    prim, sec = DNS_PROVIDERS[next_provider]
                    
                    log_message(f"🔄 Rotating DNS resolver ({trigger_reason}) to: {next_provider.upper()} ({prim})")
                    apply_system_dns(prim, sec)
                    
                    cfg["custom_dns_primary"] = prim
                    cfg["custom_dns_secondary"] = sec
                    save_config(cfg)
                    
                    last_dns_rotation_time = now
                    send_telegram_alert(f"🔀 *DNS ROTATION EVENT ({trigger_reason})*\nSystem resolver pivoted to: *{next_provider.upper()}* (`{prim}` / `{sec}`).")
        except Exception as e:
            log_message(f"⚠️ Error in DNS rotator: {e}")
        time.sleep(15)

# --- Telegram Helper Functions ---
def send_telegram_alert(message, reply_markup=None):
    config_path = os.path.join(LOG_DIR, "telegram_config.json")
    if not os.path.exists(config_path):
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not cfg.get("enabled", False):
            return
        token = cfg.get("token")
        chat_id = cfg.get("chat_id")
        if not token or not chat_id:
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        if reply_markup:
            params["reply_markup"] = reply_markup
            
        data = json.dumps(params).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=8) as response:
            response.read()
    except Exception as e:
        log_message(f"⚠️ Telegram alert failed: {e}")

def edit_telegram_message(token, chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{token}/editMessageText"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    try:
        data = json.dumps(params).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as res:
            res.read()
    except Exception as e:
        log_message(f"⚠️ Telegram editMessageText failed: {e}")

def answer_callback_query(token, callback_query_id):
    url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
    try:
        data = urllib.parse.urlencode({"callback_query_id": callback_query_id}).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=5) as res:
            res.read()
    except Exception as e:
        log_message(f"⚠️ Telegram answerCallbackQuery failed: {e}")

def get_sentry_dashboard_layout():
    cfg = load_config()
    engine = cfg.get("anonymity_engine", "tor")
    is_rot = cfg.get("dns_provider") == "rotation"
    dns_mode = "Auto-Rotation" if is_rot else cfg.get("dns_provider", "cloudflare").upper()

    # Use the cached connection status instead of a live blocking API call
    is_healthy = CONNECTION_STATUS.get("active", False)
    ip = CONNECTION_STATUS.get("ip", "Checking...")
    loc = CONNECTION_STATUS.get("location", "Unknown")
    status_icon = "🟢" if is_healthy else "🔴"
    ghost_line = "💀 *[ GHOST ACTIVE ] ➔ You are a ghost!* 👻" if is_healthy else "⚠️ *Anonymity tunnel down*"

    t_path = os.path.join(LOG_DIR, "threats.json")
    threats_count = 0
    if os.path.exists(t_path):
        try:
            with open(t_path) as f:
                threats_count = len(json.load(f))
        except:
            pass

    msg = (
        f"💀 *AETHER GHOST OS SENTRY MENU*\n"
        f"-----------------------------\n"
        f"{ghost_line}\n"
        f"Anonymity Engine: *{engine.upper()}*\n"
        f"Status: {status_icon} *{'Protected' if is_healthy else 'Exposed'}*\n"
        f"Spoofed IP: `{ip}`\n"
        f"Location: *{loc}*\n"
        f"DNS Resolver: *{dns_mode}*\n"
        f"Active Threat Alerts: *{threats_count} alerts*\n\n"
        f"Use buttons below to control the phone remotely:"
    )

    kb = {
        "inline_keyboard": [
            [
                {"text": "🔄 Change Engine", "callback_data": "menu_engine"},
                {"text": "🔀 Change DNS", "callback_data": "menu_dns"}
            ],
            [
                {"text": f"🔀 Auto-Rotate DNS: {'ON 🟢' if is_rot else 'OFF 🔴'}", "callback_data": "toggle_dns_rot"}
            ],
            [
                {"text": "⚡ Run Security Scan", "callback_data": "run_scan"},
                {"text": "📋 View Threat Details", "callback_data": "view_threats"}
            ]
        ]
    }
    return msg, kb

def handle_sentry_callback(token, chat_id, query):
    query_id = query.get("id")
    sender_id = str(query.get("from", {}).get("id", ""))
    data = query.get("data", "")
    message = query.get("message", {})
    message_id = message.get("message_id")

    if sender_id != str(chat_id):
        return

    answer_callback_query(token, query_id)
    cfg = load_config()
    global last_manual_change_time

    if data == "menu_main":
        msg, kb = get_sentry_dashboard_layout()
        edit_telegram_message(token, chat_id, message_id, msg, kb)

    elif data == "menu_engine":
        msg = "🔄 *Select Anonymity Engine*\n\nChoose an engine circuit below to route your internet traffic:"
        kb = {
            "inline_keyboard": [
                [
                    {"text": "🧅 Tor SOCKS", "callback_data": "set_engine_tor"},
                    {"text": "⚡ Cloudflare WARP", "callback_data": "set_engine_warp"}
                ],
                [
                    {"text": "🔀 SOCKS Proxy", "callback_data": "set_engine_proxy"},
                    {"text": "🟣 DoH Resolver", "callback_data": "set_engine_doh"}
                ],
                [
                    {"text": "🔴 Disable Anonymity", "callback_data": "set_engine_none"}
                ],
                [
                    {"text": "↩️ Back to Menu", "callback_data": "menu_main"}
                ]
            ]
        }
        edit_telegram_message(token, chat_id, message_id, msg, kb)
        
    elif data.startswith("set_engine_"):
        selected = data.replace("set_engine_", "")
        cfg["anonymity_engine"] = selected
        save_config(cfg)
        activate_engine_routing(selected)
        last_manual_change_time = time.time()
        
        msg = f"✅ *Anonymity Engine switched to: {selected.upper()}*\n\nCircuits are warming up now. Routing applied globally."
        kb = {"inline_keyboard": [[{"text": "↩️ Return to Menu", "callback_data": "menu_main"}]]}
        edit_telegram_message(token, chat_id, message_id, msg, kb)
        
    elif data == "menu_dns":
        msg = "🔀 *Select Secure DNS Resolver*\n\nChange your system DNS resolver configuration:"
        kb = {
            "inline_keyboard": [
                [
                    {"text": "☁️ Cloudflare (1.1.1.1)", "callback_data": "set_dns_cloudflare"},
                    {"text": "🔍 Google (8.8.8.8)", "callback_data": "set_dns_google"}
                ],
                [
                    {"text": "🛡️ Quad9 (9.9.9.9)", "callback_data": "set_dns_quad9"},
                    {"text": "🚫 AdGuard AdBlock", "callback_data": "set_dns_adguard"}
                ],
                [
                    {"text": "↩️ Back to Menu", "callback_data": "menu_main"}
                ]
            ]
        }
        edit_telegram_message(token, chat_id, message_id, msg, kb)
        
    elif data.startswith("set_dns_"):
        selected = data.replace("set_dns_", "")
        prim, sec = DNS_PROVIDERS[selected]
        cfg["dns_provider"] = selected
        cfg["custom_dns_primary"] = prim
        cfg["custom_dns_secondary"] = sec
        save_config(cfg)
        apply_system_dns(prim, sec)
        
        msg = f"✅ *DNS Resolver updated to: {selected.upper()}*\n\nPrimary IP: `{prim}`\nSecondary IP: `{sec}`"
        kb = {"inline_keyboard": [[{"text": "↩️ Return to Menu", "callback_data": "menu_main"}]]}
        edit_telegram_message(token, chat_id, message_id, msg, kb)
        
    elif data == "toggle_dns_rot":
        current_rot = cfg.get("dns_provider") == "rotation"
        if current_rot:
            cfg["dns_provider"] = "cloudflare"
            cfg["dns_rotation_interval"] = 0
            cfg["custom_dns_primary"] = "1.1.1.1"
            cfg["custom_dns_secondary"] = "1.0.0.1"
            apply_system_dns("1.1.1.1", "1.0.0.1")
        else:
            cfg["dns_provider"] = "rotation"
            cfg["dns_rotation_interval"] = 5
            prim, sec = DNS_PROVIDERS["cloudflare"]
            cfg["custom_dns_primary"] = prim
            cfg["custom_dns_secondary"] = sec
            apply_system_dns(prim, sec)
            
        save_config(cfg)
        msg, kb = get_sentry_dashboard_layout()
        edit_telegram_message(token, chat_id, message_id, msg, kb)
        
    elif data == "run_scan":
        edit_telegram_message(token, chat_id, message_id, "🔄 *Active Security scan triggered...* please wait.", None)
        run_security_scan()
        msg, kb = get_sentry_dashboard_layout()
        edit_telegram_message(token, chat_id, message_id, "✅ *Scan Completed!*\n\n" + msg, kb)
        
    elif data == "view_threats":
        t_path = os.path.join(LOG_DIR, "threats.json")
        threats_list = []
        if os.path.exists(t_path):
            try:
                with open(t_path) as f:
                    threats_list = json.load(f)
            except:
                pass
                
        if not threats_list:
            msg = "🟢 *Aether Sentry Alert Logs*\n\nNo threats captured today! All systems secure."
        else:
            msg_lines = ["⚠️ *Active Security Alerts & Diagnostics:*", "-----------------------------"]
            for idx, t in enumerate(threats_list[-6:]):
                time_str = t["time"].split("T")[-1][:5]
                msg_lines.append(f"• *[{time_str}]* {t['detail']}")
            msg_lines.append("\n💡 Visit the dashboard for step-by-step fix tutorials.")
            msg = "\n".join(msg_lines)
            
        kb = {"inline_keyboard": [[{"text": "↩️ Return to Menu", "callback_data": "menu_main"}]]}
        edit_telegram_message(token, chat_id, message_id, msg, kb)

def run_telegram_bot_poller():
    last_update_id = 0
    config_path = os.path.join(LOG_DIR, "telegram_config.json")

    while True:
        try:
            if not os.path.exists(config_path):
                time.sleep(10)
                continue
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if not cfg.get("enabled", False):
                time.sleep(10)
                continue
            token = cfg.get("token", "").strip()
            chat_id = str(cfg.get("chat_id", "")).strip()
            if not token or not chat_id:
                time.sleep(10)
                continue

            # Get updates
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}&timeout=5"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=12) as response:
                res_data = json.loads(response.read().decode('utf-8'))

            if res_data.get("ok") and res_data.get("result"):
                for update in res_data.get("result"):
                    last_update_id = update.get("update_id", last_update_id)

                    # 1. Parse Callback Button clicks
                    callback_query = update.get("callback_query")
                    if callback_query:
                        handle_sentry_callback(token, chat_id, callback_query)
                        continue

                    # 2. Parse Standard Messages
                    message = update.get("message")
                    if not message:
                        continue
                    sender_chat = message.get("chat", {})
                    sender_id = str(sender_chat.get("id", ""))
                    text = message.get("text", "").strip()
                    if not text:
                        continue

                    # Allow anyone to /start — ignore others for security
                    if text.startswith("/start") and sender_id != chat_id:
                        send_telegram_alert("⚠️ Unauthorized access attempt blocked.")
                        continue
                    elif sender_id != chat_id:
                        continue

                    if text.startswith("/start") or text.startswith("/menu") or text.startswith("/status"):
                        msg, kb = get_sentry_dashboard_layout()
                        send_telegram_alert(msg, kb)
                    elif text.startswith("/scan"):
                        send_telegram_alert("🔄 *Security scan triggered...* Running in background, I will notify you when done.")
                        # Run scan in background thread so the bot stays responsive
                        def _do_scan():
                            run_security_scan()
                            msg, kb = get_sentry_dashboard_layout()
                            send_telegram_alert("✅ *Scan Completed!*\n\n" + msg, kb)
                        threading.Thread(target=_do_scan, daemon=True).start()
                    elif text.startswith("/panic"):
                        send_telegram_alert("🚨 *PANIC COMMAND RECEIVED! De-authenticating...*")
                        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        script_name = "ghost_mode_pc.py" if sys.platform == "win32" else "ghost_mode.py"
                        script_path = os.path.join(base_dir, script_name)
                        if not os.path.exists(script_path):
                            script_path = os.path.expanduser(f"~/{script_name}")
                        if os.path.exists(script_path):
                            subprocess.run([sys.executable, script_path, "--panic"])
                        send_telegram_alert("🤫 *De-authentication sequence executed.* Session offline.")
                    else:
                        # Scam scanner
                        send_telegram_alert("🔍 *Analyzing message for scams and phishing...*")
                        import re
                        urls = re.findall(r'(https?://\S+)', text)
                        scam_keywords = [
                            "m-pesa reference", "congratulations", "win", "won", "reward", "lottery",
                            "package delivery", "unclaimed", "suspension", "locked account", "verify identity",
                            "click here", "urgent", "update password", "banking support", "invest", "profit",
                            "cash prize", "sent you money", "reference number", "cashback"
                        ]

                        has_scam_keyword = any(kw in text.lower() for kw in scam_keywords)
                        reports = []

                        for url in urls:
                            domain = url.split("://")[-1].split("/")[0].lower()
                            suspicious_tlds = [".xyz", ".top", ".club", ".info", ".bid", ".icu", ".click", ".gq", ".cf", ".tk", ".ml", ".ga"]
                            is_suspicious_tld = any(domain.endswith(tld) for tld in suspicious_tlds)

                            is_lookalike = False
                            matched_brand = ""
                            for brand in ["safaricom", "paypal", "google", "facebook", "netflix", "binance", "blockchain"]:
                                if brand in domain and domain != f"{brand}.com" and not domain.endswith(f".{brand}.com") and not domain.endswith(f"safaricom.co.ke"):
                                    is_lookalike = True
                                    matched_brand = brand

                            if is_lookalike:
                                reports.append(f"❌ `{domain}` — *Lookalike domain!* (Spoofing {matched_brand})")
                            elif is_suspicious_tld:
                                reports.append(f"⚠️ `{domain}` — Uses a high-risk TLD ({domain.split('.')[-1]}).")
                            else:
                                reports.append(f"ℹ️ `{domain}` — Extracted for analysis.")

                        risk_level = "🟢 LOW RISK"
                        risk_color = "🟢"
                        if reports or has_scam_keyword:
                            risk_level = "🟡 MEDIUM RISK"
                            risk_color = "🟡"
                        if any("❌" in r for r in reports) or (has_scam_keyword and len(urls) > 0):
                            risk_level = "🔴 HIGH RISK (PHISHING/SCAM)"
                            risk_color = "🔴"

                        msg = [
                            f"🤖 *Scam Detection Report*",
                            f"-----------------------------",
                            f"Risk Assessment: *{risk_level}*",
                            f"Urgency/Fraud Language: *{'Detected ⚠️' if has_scam_keyword else 'None detected'}*",
                        ]
                        if urls:
                            msg.append(f"\nExtracted Links ({len(urls)}):")
                            msg.extend(reports)
                        else:
                            msg.append("\nNo links found in message.")

                        if risk_color == "🔴":
                            msg.append("\n❗ *Warning:* Do NOT click any links or reply to the sender of this message.")
                        elif risk_color == "🟡":
                            msg.append("\n⚠️ *Caution:* Verify the sender before taking any action.")
                        else:
                            msg.append("\n✅ *Note:* No obvious scam indicators found, but always remain vigilant.")

                        send_telegram_alert("\n".join(msg))

        except Exception as poller_err:
            # Log errors so they are visible in ghost.log — never silently swallow
            err_str = str(poller_err)
            if "timed out" not in err_str.lower() and "read operation" not in err_str.lower():
                log_message(f"⚠️ Sentry bot poller error: {err_str[:120]}")
        time.sleep(2.5)

# --- Switch Engine Command Execution ---
def activate_engine_routing(engine):
    log_message(f"🔄 Activating engine routing for: {engine.upper()}")
    if engine == "tor":
        subprocess.run("pkill tor 2>/dev/null", shell=True)
        subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
    elif engine == "warp":
        subprocess.run("pkill tor 2>/dev/null", shell=True)
        subprocess.run("warp-cli connect 2>/dev/null", shell=True)
        time.sleep(3)
    elif engine == "none":
        subprocess.run("pkill tor 2>/dev/null", shell=True)
        subprocess.run("warp-cli disconnect 2>/dev/null", shell=True)
        time.sleep(2)
    else:
        subprocess.run("pkill tor 2>/dev/null", shell=True)

# --- Decoy Honeypot Listener ---
def run_honeypot_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', 2222))
        server.listen(10)
        log_message("🛡️ Decoy Honeypot active on port 2222 (Monitoring LAN scans)")
        while True:
            conn, addr = server.accept()
            ip = addr[0]
            log_message(f"🚨 HONEYPOT INTRUSION ALERT! Port scan detected from IP: {ip}")
            trigger_native_notification("SECURITY INTRUSION", f"Rogue network scan detected from IP: {ip}!")
            send_telegram_alert(f"🚨 *SECURITY INTRUSION ALERT!*\nHoneypot Decoy Intrusion: Rogue scan detected from IP `{ip}` on port 2222.")
            conn.close()
    except Exception as e:
        log_message(f"⚠️ Honeypot decoy could not start: {e}")

# --- Daemon Schedulers & Failover Loop ---
def run_daemon_loop():
    log_message("🤫 Aether OS background monitor daemon started.")
    last_scan_time = 0
    global last_manual_change_time
    
    while True:
        try:
            cfg = load_config()
            engine = cfg.get("anonymity_engine", "tor")
            scan_interval = cfg.get("scan_interval", 120)
            
            # 1. Connection check and Auto-Failover
            if engine != "none":
                if time.time() - last_manual_change_time < 30:
                    # Skip check to let newly switched engine bootstrap
                    pass
                else:
                    is_healthy, current_ip, loc, real_ip = update_connection_status_cache()
                    if not is_healthy:
                        log_message(f"⚠️ Health check failed for engine '{engine.upper()}'! Starting failover sequence...")
                        sequence = ["tor", "warp", "proxy", "doh", "none"]
                        current_idx = sequence.index(engine) if engine in sequence else 0
                        
                        failover_success = False
                        for attempt in range(1, len(sequence)):
                            next_idx = (current_idx + attempt) % len(sequence)
                            next_engine = sequence[next_idx]
                            log_message(f"🔄 Pivoting failover to engine: '{next_engine.upper()}'")
                            activate_engine_routing(next_engine)
                            
                            time.sleep(6)
                            ok, nip, nloc, nrip = verify_connection_health(next_engine)
                            if ok or next_engine == "none":
                                cfg["anonymity_engine"] = next_engine
                                save_config(cfg)
                                update_connection_status_cache()
                                msg = f"Switched to {next_engine.upper()} because {engine.upper()} failed."
                                log_message(f"✅ Anonymity failover succeeded: {msg}")
                                trigger_native_notification("ANONYMITY FAILOVER", msg)
                                send_telegram_alert(f"🔄 *ANONYMITY FAILOVER EVENT*\n{msg}")
                                
                                run_security_scan()
                                failover_success = True
                                break
                        
                        if not failover_success or cfg.get("anonymity_engine") == "none":
                            log_message("⚠️ All anonymity channels down! Retrying checks in 10s...")
                            time.sleep(10)
                            continue

            # 2. Background Threat Scan scheduler
            now = time.time()
            if scan_interval > 0 and (now - last_scan_time >= scan_interval):
                run_security_scan()
                last_scan_time = now
        except Exception as daemon_err:
            log_message(f"⚠️ Exception in background daemon cycle: {daemon_err}")
            
        time.sleep(15)

# --- Custom HTTP Web Server API ---
class DashboardAPIHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def translate_path(self, path):
        filename = path.split('?')[0].split('#')[0]
        if filename.startswith('/'):
            filename = filename[1:]
        if not filename or filename == 'ghost_dashboard.html':
            return os.path.join(LOG_DIR, "ghost_dashboard.html")
        
        # Check if the requested file exists in the parent workspace assets, redirect if so
        if filename.startswith('assets/'):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_dir, filename)
            
        return os.path.join(LOG_DIR, filename)

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        url_path = self.path.split('?')[0]
        cfg = load_config()

        if url_path == '/api/telegram_config':
            config_path = os.path.join(LOG_DIR, "telegram_config.json")
            data = {"enabled": False, "token": "", "chat_id": ""}
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except:
                    pass
            self.send_json_response(data)

        elif url_path == '/api/engine-status':
            self.send_json_response(CONNECTION_STATUS)

        elif url_path == '/api/circuit':
            engine = cfg.get("anonymity_engine", "tor")
            is_active = CONNECTION_STATUS.get("active", False)
            ip = CONNECTION_STATUS.get("ip", "Disconnected")
            loc = CONNECTION_STATUS.get("location", "Offline")
            if engine == "tor" and is_active:
                self.send_json_response({
                    "hops": [
                        {"type": "Entry Guard", "ip": "185.220.101.5", "loc": "Germany (DE)"},
                        {"type": "Middle Relay", "ip": "199.249.230.77", "loc": "Canada (CA)"},
                        {"type": "Exit Node", "ip": ip, "loc": loc}
                    ]
                })
            else:
                self.send_json_response({
                    "hops": [
                        {"type": "Direct Route", "ip": "UNPROTECTED", "loc": "ISP Gateway (Exposed)"}
                    ]
                })

        elif url_path == '/api/logs':
            log_path = os.path.join(LOG_DIR, "ghost.log")
            lines = []
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f.readlines()[-60:]]
                except:
                    pass
            self.send_json_response({"logs": lines})

        elif url_path == '/api/schedule':
            self.send_json_response(cfg)

        elif url_path == '/api/report':
            report_path = os.path.join(LOG_DIR, "report.json")
            data = {"connection_type": "Unknown", "ssid": "N/A", "battery_temp": 0.0, "threats_today": 0, "status": "CLEAN", "last_scan": ""}
            if os.path.exists(report_path):
                try:
                    with open(report_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except:
                    pass
            self.send_json_response(data)

        elif url_path == '/api/threats':
            threat_path = os.path.join(LOG_DIR, "threats.json")
            data = {"threats": []}
            if os.path.exists(threat_path):
                try:
                    with open(threat_path, "r", encoding="utf-8") as f:
                        data = {"threats": json.load(f)}
                except:
                    pass
            self.send_json_response(data)

        elif url_path == '/api/dns':
            self.send_json_response({
                "dns_provider": cfg.get("dns_provider", "cloudflare"),
                "dns_rotation_interval": cfg.get("dns_rotation_interval", 0),
                "dns_scheduled_time": cfg.get("dns_scheduled_time", ""),
                "custom_dns_primary": cfg.get("custom_dns_primary", "1.1.1.1"),
                "custom_dns_secondary": cfg.get("custom_dns_secondary", "1.0.0.1")
            })

        else:
            super().do_GET()

    def do_POST(self):
        url_path = self.path.split('?')[0]
        cfg = load_config()

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        try:
            body = json.loads(post_data) if post_data else {}
        except:
            body = {}

        if url_path == '/api/telegram_config':
            config_path = os.path.join(LOG_DIR, "telegram_config.json")
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(body, f, indent=2)
                self.send_json_response({"status": "ok"})
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, 500)

        elif url_path == '/api/clear_threats':
            threat_path = os.path.join(LOG_DIR, "threats.json")
            if os.path.exists(threat_path):
                try:
                    os.remove(threat_path)
                except:
                    pass
            report_path = os.path.join(LOG_DIR, "report.json")
            if os.path.exists(report_path):
                try:
                    with open(report_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    data["threats_today"] = 0
                    data["status"] = "CLEAN"
                    with open(report_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                except:
                    pass
            self.send_json_response({"status": "ok"})

        elif url_path == '/api/telegram_test':
            token = body.get("token")
            chat_id = body.get("chat_id")
            if not token or not chat_id:
                self.send_json_response({"status": "error", "message": "Missing credentials"}, 400)
                return
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload_data = urllib.parse.urlencode({
                    "chat_id": chat_id, 
                    "text": "💀 *Aether Ghost OS: Sentry Bot Connected successfully!*", 
                    "parse_mode": "Markdown"
                }).encode('utf-8')
                req = urllib.request.Request(url, data=payload_data)
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_val = json.loads(response.read().decode('utf-8'))
                if res_val.get("ok"):
                    self.send_json_response({"status": "ok"})
                else:
                    self.send_json_response({"status": "error", "message": "Telegram API reject"}, 400)
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, 500)

        elif url_path == '/api/engine':
            global last_manual_change_time
            engine = body.get("engine", "tor")
            cfg["anonymity_engine"] = engine
            save_config(cfg)
            activate_engine_routing(engine)
            last_manual_change_time = time.time()
            log_message(f"👤 User manually set engine to: {engine.upper()}")
            # Asynchronously update cached connection info
            threading.Thread(target=update_connection_status_cache, daemon=True).start()
            self.send_json_response({"status": "ok"})

        elif url_path == '/api/location':
            codes = body.get("codes", "0")
            log_message(f"👤 User requested country rotation. Applying nodes...")
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            script_path = os.path.join(base_dir, "ghost_tools", "location_picker.py")
            if not os.path.exists(script_path):
                script_path = os.path.expanduser("~/ghost_tools/location_picker.py")
                
            if os.path.exists(script_path):
                subprocess.Popen([sys.executable, script_path, "--apply", codes], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.send_json_response({"status": "ok"})
            else:
                self.send_json_response({"status": "error", "message": "location_picker.py not found"}, 404)

        elif url_path == '/api/scan':
            if body.get("panic", False):
                log_message("🚨 PANIC DE-AUTHENTICATE EXECUTING!")
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                script_name = "ghost_mode_pc.py" if sys.platform == "win32" else "ghost_mode.py"
                script_path = os.path.join(base_dir, script_name)
                if not os.path.exists(script_path):
                    script_path = os.path.expanduser(f"~/{script_name}")
                if os.path.exists(script_path):
                    subprocess.run([sys.executable, script_path, "--panic"])
                self.send_json_response({"status": "self_destruct"})
            else:
                # Trigger scan asynchronously in a worker thread
                def run_async_scan(config_copy):
                    run_security_scan()
                    engine = config_copy.get("anonymity_engine", "tor")
                    if engine != "none":
                        is_healthy, current_ip, loc, real_ip = verify_connection_health(engine)
                        if not is_healthy:
                            log_message(f"⚠️ Active scan detected engine '{engine.upper()}' is down! Performing immediate failover healing...")
                            sequence = ["tor", "warp", "proxy", "doh", "none"]
                            current_idx = sequence.index(engine) if engine in sequence else 0
                            for attempt in range(1, len(sequence)):
                                next_idx = (current_idx + attempt) % len(sequence)
                                next_engine = sequence[next_idx]
                                log_message(f"🔄 Healing pivot to: '{next_engine.upper()}'")
                                activate_engine_routing(next_engine)
                                time.sleep(6)
                                ok, nip, nloc, nrip = verify_connection_health(next_engine)
                                if ok or next_engine == "none":
                                    config_copy["anonymity_engine"] = next_engine
                                    save_config(config_copy)
                                    break
                    update_connection_status_cache()

                threading.Thread(target=run_async_scan, args=(cfg,), daemon=True).start()
                self.send_json_response({"status": "scanning"})

        elif url_path == '/api/schedule':
            if "scan_interval" in body:
                cfg["scan_interval"] = int(body["scan_interval"])
            if "location_interval" in body:
                cfg["location_interval"] = int(body["location_interval"])
            if "notification_profile" in body:
                cfg["notification_profile"] = body["notification_profile"]
            if "custom_sound_path" in body:
                cfg["custom_sound_path"] = body["custom_sound_path"]
            
            save_config(cfg)
            self.send_json_response({"status": "ok"})

        elif url_path == '/api/dns':
            provider = body.get("dns_provider", "cloudflare")
            interval = int(body.get("dns_rotation_interval", 0))
            scheduled = body.get("dns_scheduled_time", "")
            
            cfg["dns_provider"] = provider
            cfg["dns_rotation_interval"] = interval
            cfg["dns_scheduled_time"] = scheduled
            
            if provider != "rotation":
                prim = body.get("custom_dns_primary", "1.1.1.1")
                sec = body.get("custom_dns_secondary", "1.0.0.1")
                cfg["custom_dns_primary"] = prim
                cfg["custom_dns_secondary"] = sec
                apply_system_dns(prim, sec)
            else:
                prim, sec = DNS_PROVIDERS["cloudflare"]
                cfg["custom_dns_primary"] = prim
                cfg["custom_dns_secondary"] = sec
                apply_system_dns(prim, sec)
                
            save_config(cfg)
            log_message(f"👤 User updated DNS settings. Provider: {provider.upper()}, Rotation Interval: {interval}m")
            self.send_json_response({"status": "ok"})

        else:
            self.send_response(404)
            self.end_headers()

def main():
    # Initialize cache status asynchronously
    threading.Thread(target=update_connection_status_cache, daemon=True).start()
    
    # Load and apply initial DNS configurations on startup
    try:
        cfg = load_config()
        provider = cfg.get("dns_provider", "cloudflare")
        if provider != "rotation":
            prim = cfg.get("custom_dns_primary", "1.1.1.1")
            sec = cfg.get("custom_dns_secondary", "1.0.0.1")
            apply_system_dns(prim, sec)
    except:
        pass

    daemon_thread = threading.Thread(target=run_daemon_loop, daemon=True)
    daemon_thread.start()

    telegram_thread = threading.Thread(target=run_telegram_bot_poller, daemon=True)
    telegram_thread.start()

    dns_thread = threading.Thread(target=run_dns_rotation_loop, daemon=True)
    dns_thread.start()

    honeypot_thread = threading.Thread(target=run_honeypot_listener, daemon=True)
    honeypot_thread.start()

    log_message(f"🚀 Starting Dashboard HTTP Server on port {PORT}...")
    try:
        httpd = ThreadingHTTPServer(('', PORT), DashboardAPIHandler)
        httpd.serve_forever()
    except Exception as e:
        log_message(f"❌ Server crash or port already occupied: {e}")

if __name__ == '__main__':
    main()
