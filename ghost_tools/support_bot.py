#!/usr/bin/env python3
"""
🤖 AETHER GHOST OS — Standalone Sentry Support Bot
====================================================
A lightweight, dependency-free Telegram bot you can run independently
of the main dashboard daemon. Uses only Python stdlib (urllib).

Commands:
  /start   — Show main control menu
  /menu    — Show main control menu
  /status  — Check current connection + threat summary
  /scan    — Trigger a full security scan
  /panic   — Emergency: wipe all local logs and config
  (any text) → Scam / phishing message analysis

Usage:
  python3 ghost_tools/support_bot.py
"""

import os
import sys
import json
import time
import subprocess
import threading
import urllib.request
import urllib.parse
from datetime import datetime

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

VERSION = "1.2.0"

# ── Path resolution ────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(BASE_DIR, "ghost_tools")
os.makedirs(TOOLS_DIR, exist_ok=True)

CONFIG_PATH   = os.path.join(TOOLS_DIR, "telegram_config.json")
SCHEDULE_PATH = os.path.join(TOOLS_DIR, "schedule_config.json")
THREATS_PATH  = os.path.join(TOOLS_DIR, "threats.json")
REPORT_PATH   = os.path.join(TOOLS_DIR, "report.json")
LOG_PATH      = os.path.join(TOOLS_DIR, "ghost.log")


# ── Helpers ────────────────────────────────────────────────────────
def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_telegram_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"enabled": False, "token": "", "chat_id": ""}


def load_schedule():
    if os.path.exists(SCHEDULE_PATH):
        try:
            with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def api_call(token, method, params=None):
    """Make a Telegram Bot API call using urllib only."""
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(params or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"⚠️ Telegram API error ({method}): {e}")
        return {}


def send_message(token, chat_id, text, reply_markup=None):
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    api_call(token, "sendMessage", params)


def edit_message(token, chat_id, message_id, text, reply_markup=None):
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    api_call(token, "editMessageText", params)


def answer_callback(token, callback_id):
    api_call(token, "answerCallbackQuery", {"callback_query_id": callback_id})


# ── Menu builder ───────────────────────────────────────────────────
def build_main_menu():
    sched   = load_schedule()
    engine  = sched.get("anonymity_engine", "tor").upper()
    scan_m  = sched.get("scan_mode", "interval").upper()
    threats = 0
    if os.path.exists(THREATS_PATH):
        try:
            with open(THREATS_PATH) as f:
                threats = len(json.load(f))
        except Exception:
            pass

    text = (
        f"💀 *AETHER GHOST OS SENTRY BOT* v{VERSION}\n"
        f"-----------------------------\n"
        f"Anonymity Engine: *{engine}*\n"
        f"Scheduler: *{scan_m}*\n"
        f"Active Alerts: *{threats}*\n\n"
        f"Use the buttons below to control your system remotely:"
    )
    kb = {
        "inline_keyboard": [
            [
                {"text": "💀 Run Security Scan", "callback_data": "bot_run_scan"},
                {"text": "📋 View Threat Logs",  "callback_data": "bot_view_threats"},
            ],
            [
                {"text": "🦠 Scan Memory",    "callback_data": "bot_scan_virus"},
                {"text": "💾 Scan Storage",   "callback_data": "bot_scan_malware"},
            ],
            [
                {"text": "📋 View Last Logs", "callback_data": "bot_view_logs"},
                {"text": "📥 Pull Updates",   "callback_data": "bot_pull_update"},
            ],
            [
                {"text": "🚨 PANIC",          "callback_data": "bot_panic_prompt"},
                {"text": "☕ Support & Donate","callback_data": "bot_support"},
            ],
        ]
    }
    return text, kb


# ── Scan runner ────────────────────────────────────────────────────
def run_scan_subprocess(flag=""):
    script = "ghost_mode_pc.py" if sys.platform == "win32" else "ghost_mode.py"
    script_path = os.path.join(BASE_DIR, script)
    if not os.path.exists(script_path):
        return {"status": "error", "active_threats": []}
    args = [sys.executable, script_path]
    if flag:
        args.append(flag)
    try:
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH) as f:
                return json.load(f)
    except Exception as e:
        log(f"⚠️ Scan subprocess error: {e}")
    return {"status": "error", "active_threats": []}


# ── Callback handler ───────────────────────────────────────────────
def handle_callback(token, chat_id, query):
    qid     = query.get("id")
    data    = query.get("data", "")
    msg_obj = query.get("message", {})
    msg_id  = msg_obj.get("message_id")
    sender  = str(query.get("from", {}).get("id", ""))

    answer_callback(token, qid)

    if sender != str(chat_id):
        return  # Ignore unauthorized users

    if data == "bot_main":
        text, kb = build_main_menu()
        edit_message(token, chat_id, msg_id, text, kb)

    elif data == "bot_run_scan":
        edit_message(token, chat_id, msg_id, "🔄 *Running full security scan...* please wait.", None)
        rep = run_scan_subprocess()
        status = rep.get("status", "CLEAN")
        threats_n = rep.get("threats_today", 0)
        result = "✅ *All systems secure — you are a ghost!* 👻" if status == "CLEAN" else f"⚠️ *{threats_n} threat(s) detected!* Check logs."
        text, kb = build_main_menu()
        edit_message(token, chat_id, msg_id, f"*Scan complete!*\n{result}\n\n" + text, kb)

    elif data == "bot_scan_virus":
        edit_message(token, chat_id, msg_id, "🦠 *Virus Guard memory scan running...* please wait.", None)
        run_scan_subprocess("--virus")
        text, kb = build_main_menu()
        edit_message(token, chat_id, msg_id, "✅ *Virus Guard scan complete!*\n\n" + text, kb)

    elif data == "bot_scan_malware":
        edit_message(token, chat_id, msg_id, "💾 *Malware Guard storage scan running...* please wait.", None)
        run_scan_subprocess("--malware")
        text, kb = build_main_menu()
        edit_message(token, chat_id, msg_id, "✅ *Malware Guard scan complete!*\n\n" + text, kb)

    elif data == "bot_view_threats":
        threats_list = []
        if os.path.exists(THREATS_PATH):
            try:
                with open(THREATS_PATH) as f:
                    threats_list = json.load(f)
            except Exception:
                pass
        if not threats_list:
            text = "🟢 *No threats recorded.* All systems secure!"
        else:
            lines = ["⚠️ *Last 5 Security Alerts:*\n"]
            for i, t in enumerate(threats_list[-5:], 1):
                ts = t.get("time", "")[:16].replace("T", " ")
                lines.append(f"*{i}.* [{ts}] {t.get('detail', '')}")
            text = "\n".join(lines)
        kb = {"inline_keyboard": [[{"text": "↩️ Back", "callback_data": "bot_main"}]]}
        edit_message(token, chat_id, msg_id, text, kb)

    elif data == "bot_view_logs":
        lines_out = "No logs yet."
        if os.path.exists(LOG_PATH):
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    lines_out = "".join(f.readlines()[-12:])
            except Exception:
                pass
        text = f"📋 *Last 12 Log Lines:*\n```\n{lines_out}\n```"
        kb = {"inline_keyboard": [[{"text": "↩️ Back", "callback_data": "bot_main"}]]}
        edit_message(token, chat_id, msg_id, text, kb)

    elif data == "bot_pull_update":
        edit_message(token, chat_id, msg_id, "🔄 *Checking for updates...* please wait.", None)
        base = BASE_DIR
        if not os.path.isdir(os.path.join(base, ".git")):
            kb = {"inline_keyboard": [[{"text": "↩️ Back", "callback_data": "bot_main"}]]}
            edit_message(token, chat_id, msg_id,
                         "ℹ️ *Installed via ZIP.* Re-download from GitHub to update:\nhttps://github.com/AETHERGHOSTOS/ghost-mode", kb)
            return
        try:
            subprocess.run("git fetch", shell=True, capture_output=True, timeout=15, cwd=base)
            local  = subprocess.run("git rev-parse HEAD",  shell=True, capture_output=True, text=True, cwd=base).stdout.strip()
            remote = subprocess.run("git rev-parse @{u}", shell=True, capture_output=True, text=True, cwd=base).stdout.strip()
            if local == remote:
                msg = "🟢 *Already up-to-date!*"
            else:
                pull = subprocess.run("git pull", shell=True, capture_output=True, text=True, timeout=30, cwd=base)
                msg = "✅ *Update pulled successfully!* Restart the bot to apply." if pull.returncode == 0 else f"❌ Pull failed:\n`{pull.stderr.strip()}`"
        except Exception as e:
            msg = f"❌ Update error: `{e}`"
        kb = {"inline_keyboard": [[{"text": "↩️ Back", "callback_data": "bot_main"}]]}
        edit_message(token, chat_id, msg_id, msg, kb)

    elif data == "bot_panic_prompt":
        text = "⚠️ *CONFIRM PANIC SELF-DESTRUCT*\n\nDelete ALL local logs, config and security profiles?"
        kb = {"inline_keyboard": [
            [{"text": "🚨 YES, DESTRUCT!", "callback_data": "bot_panic_confirm"},
             {"text": "❌ NO, CANCEL",     "callback_data": "bot_main"}]
        ]}
        edit_message(token, chat_id, msg_id, text, kb)

    elif data == "bot_panic_confirm":
        edit_message(token, chat_id, msg_id, "🤫 *Panic destruct executing...*", None)
        for fname in ["ghost.log", "report.json", "threats.json",
                      "schedule_config.json", "telegram_config.json", "dashboard_token.txt"]:
            p = os.path.join(TOOLS_DIR, fname)
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        send_message(token, chat_id,
                     "💀 *Panic destruct complete.* All local data wiped. Bot shutting down.")
        log("💀 PANIC destruct executed via Sentry Bot. Exiting.")
        sys.exit(0)

    elif data == "bot_support":
        text = (
            "☕ *Support Aether Ghost OS Development*\n\n"
            "🔗 *Buy Me a Coffee:* [buymeacoffee.com/aetherghost.os](https://buymeacoffee.com/aetherghost.os)\n\n"
            "🪙 *Crypto Addresses:*\n"
            "• *USDT (TRC20):* `TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU`\n"
            "• *USDC (Solana):* `9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui`\n"
            "• *USDT/BNB (ERC20/BEP20):* `0x09cad574c2c39a88ce931307361682680b795490`\n"
            "• *BTC Native:* `15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k`\n"
            "• *BTC SegWit:* `bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj`\n\n"
            "Thank you for keeping Aether Ghost OS alive! 💀"
        )
        kb = {"inline_keyboard": [[{"text": "↩️ Back", "callback_data": "bot_main"}]]}
        edit_message(token, chat_id, msg_id, text, kb)


# ── Scam analyser ──────────────────────────────────────────────────
def analyse_scam(text):
    import re
    urls = re.findall(r"(https?://\S+)", text)
    scam_kw = [
        "m-pesa reference", "congratulations", "won", "win", "reward", "lottery",
        "package delivery", "unclaimed", "suspension", "locked account", "verify identity",
        "click here", "urgent", "update password", "banking support", "invest",
        "cash prize", "sent you money", "reference number", "cashback",
    ]
    bad_tlds    = {".xyz", ".top", ".club", ".info", ".bid", ".icu", ".click",
                   ".gq", ".cf", ".tk", ".ml", ".ga"}
    brands      = ["safaricom", "paypal", "google", "facebook", "netflix", "binance", "blockchain"]

    has_kw   = any(k in text.lower() for k in scam_kw)
    reports  = []

    for url in urls:
        domain = url.split("://")[-1].split("/")[0].lower()
        tld    = "." + domain.rsplit(".", 1)[-1] if "." in domain else ""
        lookalike = next((b for b in brands
                          if b in domain and domain not in (f"{b}.com", f"{b}.co.ke")), None)
        if lookalike:
            reports.append(f"❌ `{domain}` — Lookalike domain! (Spoofing {lookalike})")
        elif tld in bad_tlds:
            reports.append(f"⚠️ `{domain}` — High-risk TLD ({tld})")
        else:
            reports.append(f"ℹ️ `{domain}` — Extracted for analysis")

    if any("❌" in r for r in reports) or (has_kw and urls):
        risk = "🔴 HIGH RISK (PHISHING/SCAM)"
        note = "❗ *Do NOT click any links or reply to this sender.*"
    elif reports or has_kw:
        risk = "🟡 MEDIUM RISK"
        note = "⚠️ *Verify the sender before taking any action.*"
    else:
        risk = "🟢 LOW RISK"
        note = "✅ No obvious scam indicators, but always stay vigilant."

    lines = [
        "🤖 *Scam Detection Report*",
        f"Risk: *{risk}*",
        f"Fraud language: *{'Detected ⚠️' if has_kw else 'None'}*",
    ]
    if urls:
        lines.append(f"\nExtracted links ({len(urls)}):")
        lines.extend(reports)
    else:
        lines.append("\nNo links found.")
    lines.append(f"\n{note}")
    return "\n".join(lines)


# ── Main polling loop ──────────────────────────────────────────────
def run_bot():
    cfg = load_telegram_config()
    if not cfg.get("enabled"):
        print("⚠️  Sentry Bot is not enabled.")
        print("   Enable it via the dashboard or ghost_mode_pc.py → Option 14.")
        sys.exit(1)

    token   = cfg.get("token", "").strip()
    chat_id = str(cfg.get("chat_id", "")).strip()

    if not token or not chat_id:
        print("❌ Bot token or chat ID is missing in telegram_config.json.")
        sys.exit(1)

    log(f"🤖 Aether Ghost OS Sentry Bot started (standalone mode)")
    log(f"   Monitoring chat: {chat_id}")

    # Send startup notification
    send_message(token, chat_id,
                 f"🤖 *Aether Ghost OS Sentry Bot online!* v{VERSION}\n"
                 f"Type /menu to open the control panel.")

    last_update_id = 0
    while True:
        try:
            url = (f"https://api.telegram.org/bot{token}/getUpdates"
                   f"?offset={last_update_id + 1}&timeout=5")
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    last_update_id = update.get("update_id", last_update_id)

                    # Button callbacks
                    cb = update.get("callback_query")
                    if cb:
                        handle_callback(token, chat_id, cb)
                        continue

                    # Text messages
                    msg = update.get("message")
                    if not msg:
                        continue
                    sender_id = str(msg.get("chat", {}).get("id", ""))
                    text      = msg.get("text", "").strip()
                    if not text:
                        continue

                    # Block unauthorized users
                    if sender_id != chat_id:
                        if text.startswith("/start"):
                            send_message(token, chat_id, "⚠️ Unauthorized access attempt blocked.")
                        continue

                    if text.startswith(("/start", "/menu", "/status")):
                        menu_text, kb = build_main_menu()
                        send_message(token, chat_id, menu_text, kb)

                    elif text.startswith("/scan"):
                        send_message(token, chat_id,
                                     "🔄 *Security scan triggered...* I'll notify you when done.")
                        def _scan():
                            rep = run_scan_subprocess()
                            st = rep.get("status", "CLEAN")
                            n  = rep.get("threats_today", 0)
                            r  = "✅ All clear — ghost active! 👻" if st == "CLEAN" else f"⚠️ {n} threat(s) found!"
                            send_message(token, chat_id, f"*Scan complete!*\n{r}")
                        threading.Thread(target=_scan, daemon=True).start()

                    elif text.startswith("/panic"):
                        send_message(token, chat_id, "🚨 *Panic received!* Reply `/confirmpanic` to execute destruct.")

                    elif text.startswith("/confirmpanic"):
                        send_message(token, chat_id, "💀 *Executing panic destruct...*")
                        for fname in ["ghost.log", "report.json", "threats.json",
                                      "schedule_config.json", "telegram_config.json", "dashboard_token.txt"]:
                            p = os.path.join(TOOLS_DIR, fname)
                            if os.path.exists(p):
                                try:
                                    os.remove(p)
                                except Exception:
                                    pass
                        send_message(token, chat_id, "🤫 *Destruct complete.* All data wiped. Bot offline.")
                        log("💀 PANIC destruct via /confirmpanic. Exiting.")
                        sys.exit(0)

                    else:
                        # Scam analysis for any other message
                        send_message(token, chat_id, "🔍 *Analysing for scams and phishing...*")
                        send_message(token, chat_id, analyse_scam(text))

        except Exception as e:
            err = str(e)
            if "timed out" not in err.lower() and "read operation" not in err.lower():
                log(f"⚠️ Bot poller error: {err[:120]}")
        time.sleep(2)


if __name__ == "__main__":
    run_bot()
