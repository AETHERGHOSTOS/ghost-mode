#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import time
import os

# ═══════════════════════════════════════════════════
# AETHER GHOST OS — PROFESSIONAL TELEGRAM SUPPORT BOT
# ═══════════════════════════════════════════════════
# Pure Python — Zero Dependencies (runs on any phone/PC with Python 3)
# Features:
# 1. Custom Button Menu (Reply Keyboard) for visitors.
# 2. Automated Welcome, About, FAQ, and Live Donation cards.
# 3. Message forwarding to Operator and 2-way reply mapping.
# ═══════════════════════════════════════════════════

# Configuration Files
CONFIG_FILE = "bot_config.json"
DATA_FILE = "bot_data.json"

# Default configuration template
DEFAULT_CONFIG = {
    "BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",  # Replace with token from @BotFather
    "ADMIN_CHAT_ID": None,                  # Auto-registered on first /start command
    "ADMIN_PASSCODE": "CHANGE_ME_NOW",      # Send '/start YOUR_PASSCODE' to register
    "IS_ONLINE": False                      # Toggle with /online and /offline
}

# Real Donation Info & Project Details
RESPONSES = {
    "welcome_offline": (
        "🤖 *Aether Ghost OS Auto-Responder*\n\n"
        "Hello! Thanks for contacting The Ghost Support.\n"
        "The operator is currently *OFFLINE* (coding or offline).\n\n"
        "💡 *Quick Options:*\n"
        "• Tap buttons below to get instant download instructions, FAQs, or project info.\n"
        "• Tap *💬 Talk to Developer* to drop a question or message, and we'll reply when online!"
    ),
    "welcome_online": (
        "🤖 *Aether Ghost OS Support*\n\n"
        "Hello! The operator is currently *ONLINE*.\n"
        "Tap the menu buttons below or type your query directly. We are ready to assist you!"
    ),
    "about": (
        "🛡️ *About Aether Ghost OS & Ecosystem*\n\n"
        "Developed by *AETHERGHOSTOS Corp*, Aether is a unified, sovereign privacy ecosystem designed to secure all your personal devices and networks. It runs locally and sandbox-isolated inside user-space, focusing on complete privacy and absolute digital sovereignty without requiring root access or sending your data to any cloud servers.\n\n"
        "*Core Modules (Simplified):*\n"
        "• *Deception Sentry:* Traps and delays unauthorized network scans on port `2222` with a decoy SSH tarpit honeypot, reporting intrusions instantly.\n"
        "• *Sovereign Tor Routing:* Hides your connection and IP location using rotational multi-country Tor proxy circuits.\n"
        "• *Privacy Sentry (Hardware Audits):* Monitors Windows/Android camera and microphone log access in real-time to detect spy apps.\n"
        "• *Scam & Phishing Sentry:* Offline-compatible link and message scanner running inside Telegram to audit incoming texts for fraud.\n"
        "• *Active Failover Daemon:* Automatically switches connection routing between Tor, Cloudflare WARP, and secure DNS if channels drop.\n"
        "• *Stealth Mode (Panic Switch):* Instant log cleaning and tunnel shutdowns via local controls or remote Telegram `/panic` commands.\n\n"
        "🔮 *Roadmap & Next Updates:*\n"
        "• *[COMPLETED]* Setup Installer & Termux:API signature alignment.\n"
        "• *[COMPLETED]* Local HTML Dashboard Sentry Console.\n"
        "• *[COMPLETED]* Telegram Sentry Integration (Remote commands & Scam scanner).\n"
        "• *[COMPLETED]* Customer Support Bot Framework (`support_bot.py`).\n"
        "• *[PLANNED]* Desktop Sentry Apps (Workstation editions).\n"
        "• *[PLANNED]* Hardened OS Builds & Physical Killswitch Accessories.\n\n"
        "💡 *What features do you want to see next?*\n"
        "We build Aether for you. If you have an idea, a feature request, or a custom tool you need, tap *💬 Talk to Developer* right now and send us your thoughts!"
    ),
    "download": (
        "📁 *Aether Ghost OS Downloads & Guides*\n\n"
        "Aether Ghost OS supports multiple operating systems (Android/Termux, Linux, PC).\n\n"
        "Please visit our public GitHub repository to find the specific installation guide for your platform:\n\n"
        "🔗 *GitHub Repository:* https://github.com/AETHERGHOSTOS/ghost-mode\n\n"
        "💡 Review the README.md in the repository homepage to select your platform and copy setup commands."
    ),
    "community": (
        "💬 *Aether Ghost OS Community Channels*\n\n"
        "• *Telegram Group:* [Aether Operator OS Command](https://t.me/AetherOperatorOSCommand) *(Chat)*\n"
        "• *Discord Community:* https://discord.gg/gNdeFA984\n"
        "• *Proton Mail:* AETHERGHOSTOS@proton.me\n"
        "• *1-on-1 Support:* Message this bot directly! (Just type your question below)"
    ),
    "talk_to_developer": (
        "💬 *Talk to Aether Developer / Support*\n\n"
        "Have a custom, complex question, or feedback?\n\n"
        "✍️ *Type your message below and send it.* The bot will instantly forward your query to the developer's private screen, and they will reply to you directly in this chat!"
    ),
    "donate": (
        "💸 *Support Aether Ghost OS*\n\n"
        "Contributions help us fund server relays, active audits, and open-source packages. You can copy any address below:\n\n"
        "• *USDT (TRC-20):*\n`TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU`\n"
        "• *USDC (Solana):*\n`9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui`\n"
        "• *USDT (ERC-20):*\n`0x09cad574c2c39a88ce931307361682680b795490`\n"
        "• *BNB (BEP-20):*\n`0x09cad574c2c39a88ce931307361682680b795490`\n"
        "• *BNB (ERC-20):*\n`0x09cad574c2c39a88ce931307361682680b795490`\n"
        "• *Bitcoin (Native BTC):*\n`15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k`\n"
        "• *Bitcoin (BEP-20):*\n`0x09cad574c2c39a88ce931307361682680b795490`\n"
        "• *Bitcoin (ERC-20):*\n`0x09cad574c2c39a88ce931307361682680b795490`\n"
        "• *Bitcoin (SegWit):*\n`bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj`\n\n"
        "💳 *Fiat / Card:*\n"
        "• [Buy Me a Coffee](https://buymeacoffee.com/aetherghost.os)"
    ),
    "faq": (
        "🔒 *Frequently Asked Questions*\n\n"
        "*Q: Does this require root access?*\n"
        "A: No, Aether runs entirely in user-space sandbox isolation via Termux on Android, and as standard packages on Linux/PC.\n\n"
        "*Q: Will this drain my battery?*\n"
        "A: Aether is highly optimized. Battery usage is minimal. The daemon runs a lightweight scan in under 5 seconds every 2 minutes.\n\n"
        "*Q: Is it open source?*\n"
        "A: Yes! The core codebase, installers, Sentry systems, and HTML dashboard are open-source and hosted on our public GitHub repository."
    )
}

# Custom Menu buttons
VISITOR_KEYBOARD = {
    "keyboard": [
        [{"text": "🛡️ About Aether"}, {"text": "📁 Download & Setup"}],
        [{"text": "🔒 Read FAQs"}, {"text": "💬 Talk to Developer"}],
        [{"text": "💸 Donate / Support"}, {"text": "💬 Join Community"}]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

class AetherSupportBot:
    def __init__(self):
        self.config = self.load_json(CONFIG_FILE, DEFAULT_CONFIG)
        self.data = self.load_json(DATA_FILE, {"mappings": {}, "clients": {}})
        self.token = self.config.get("BOT_TOKEN")
        self.admin_id = self.config.get("ADMIN_CHAT_ID")
        self.passcode = self.config.get("ADMIN_PASSCODE")
        self.is_online = self.config.get("IS_ONLINE", False)
        
        if not self.token or self.token == "YOUR_TELEGRAM_BOT_TOKEN":
            print("[!] ERROR: Please set your BOT_TOKEN in bot_config.json")
            print("[!] Get a bot token by messaging @BotFather on Telegram.")
        else:
            print(f"[*] Aether Support Bot initialized.")
            print(f"[*] Current Mode: {'ONLINE (Real-time)' if self.is_online else 'OFFLINE (Auto-reply)'}")
            if self.admin_id:
                print(f"[*] Registered Admin ID: {self.admin_id}")
            else:
                print(f"[!] Warning: No Admin registered. Send '/start {self.passcode}' to the bot to claim control.")

    def load_json(self, filepath, default):
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=4)
            return default
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default

    def save_json(self, filepath, data):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[!] Error saving {filepath}: {e}")

    def save_config(self):
        self.config["BOT_TOKEN"] = self.token
        self.config["ADMIN_CHAT_ID"] = self.admin_id
        self.config["IS_ONLINE"] = self.is_online
        self.save_json(CONFIG_FILE, self.config)

    def api_call(self, method, params=None):
        url = f"https://api.telegram.org/bot{self.token}/{method}"
        data = None
        headers = {}
        
        if params:
            data = json.dumps(params).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            
        req = urllib.request.Request(url, data=data, headers=headers, method='POST' if data else 'GET')
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            # Suppress standard long-polling socket timeout messages to keep terminal clean
            if "timed out" not in str(e).lower():
                print(f"[!] API Error on {method}: {e}")
            return None

    def send_message(self, chat_id, text, parse_mode="Markdown", reply_to_message_id=None, reply_markup=None):
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        return self.api_call("sendMessage", params)

    def handle_admin_command(self, text, message_id, chat_id):
        parts = text.split()
        cmd = parts[0].lower()
        
        if cmd == "/start":
            param = text[len("/start"):].strip()
            if param == self.passcode:
                self.admin_id = self.admin_id or chat_id
                self.send_message(self.admin_id, f"✅ Admin registered successfully! ID: {self.admin_id}\n\n*Available Commands:*\n• /online - Go online (turn off auto-responder)\n• /offline - Go offline (enable auto-responder)\n• /status - Check system status")
                self.save_config()
            elif self.admin_id:
                self.send_message(self.admin_id, "🤖 Admin session active. Use /online or /offline to toggle status.")
                
        elif cmd == "/online":
            self.is_online = True
            self.send_message(self.admin_id, "🟢 *Status: ONLINE*\nAuto-responder is disabled. You are chatting with clients in real-time.")
            self.save_config()
            
        elif cmd == "/offline":
            self.is_online = False
            self.send_message(self.admin_id, "🔴 *Status: OFFLINE*\nAuto-responder enabled. Clients will get the offline message, and their queries will be forwarded here.")
            self.save_config()
            
        elif cmd == "/status":
            status_str = "🟢 ONLINE (Real-time)" if self.is_online else "🔴 OFFLINE (Auto-reply)"
            engine_str = "⚠️ UNPROTECTED (Shield Disabled)"
            config_path = os.path.expanduser("~/ghost_tools/schedule_config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                    engine = cfg.get("anonymity_engine", "none")
                    if engine != "none":
                        engine_str = f"*[ GHOST ACTIVE ] ➔ You are a ghost!* 👻 ({engine.upper()} active)"
                except:
                    pass
            self.send_message(self.admin_id, f"ℹ️ *Aether Bot Status*\n• Support Mode: {status_str}\n• Anonymity Shield: {engine_str}\n• Clients Logged: {len(self.data['clients'])}")

    def handle_admin_reply(self, message):
        # We need to find which user this message was a reply to.
        reply_to = message.get("reply_to_message")
        if not reply_to:
            self.send_message(self.admin_id, "💡 *Tip:* To reply to a client, you must use Telegram's 'Reply' feature directly on their forwarded message.")
            return

        fwd_msg_id = str(reply_to.get("message_id"))
        client_chat_id = self.data["mappings"].get(fwd_msg_id)
        
        if not client_chat_id:
            self.send_message(self.admin_id, "❌ Error: Could not link this reply to any active client. The session may have expired.")
            return

        # Send the admin's reply to the client
        text = message.get("text", "")
        # Forward text or other media types
        result = self.send_message(client_chat_id, text, parse_mode="Markdown")
        if result and result.get("ok"):
            self.send_message(self.admin_id, f"✅ Message sent to client.")
        else:
            self.send_message(self.admin_id, f"❌ Failed to deliver message to client (User might have blocked the bot).")

    def handle_client_message(self, message, chat_id, first_name, username):
        text = message.get("text", "")
        msg_id = message.get("message_id")
        
        # Check standard commands or button text clicks
        clean_text = text.strip()
        cmd = clean_text.lower()
        
        if cmd == "/start":
            welcome_msg = RESPONSES["welcome_online"] if self.is_online else RESPONSES["welcome_offline"]
            self.send_message(chat_id, welcome_msg, reply_markup=VISITOR_KEYBOARD)
            
            # Log client
            self.data["clients"][str(chat_id)] = {"name": first_name, "username": username, "last_seen": time.time()}
            self.save_json(DATA_FILE, self.data)
            
            # Notify admin of new chat start
            if self.admin_id:
                self.send_message(self.admin_id, f"👤 *New Visitor started chat:*\n• Name: {first_name}\n• User: @{username or 'None'}\n• Chat ID: `{chat_id}`")
            return
            
        elif cmd == "/download" or clean_text == "📁 Download & Setup":
            self.send_message(chat_id, RESPONSES["download"], reply_markup=VISITOR_KEYBOARD)
            return
        elif cmd == "/community" or clean_text == "💬 Join Community":
            self.send_message(chat_id, RESPONSES["community"], reply_markup=VISITOR_KEYBOARD)
            return
        elif cmd == "/faq" or clean_text == "🔒 Read FAQs":
            self.send_message(chat_id, RESPONSES["faq"], reply_markup=VISITOR_KEYBOARD)
            return
        elif cmd == "/about" or clean_text == "🛡️ About Aether":
            self.send_message(chat_id, RESPONSES["about"], reply_markup=VISITOR_KEYBOARD)
            return
        elif cmd == "💬 Talk to Developer":
            self.send_message(chat_id, RESPONSES["talk_to_developer"], reply_markup=VISITOR_KEYBOARD)
            return
        elif cmd == "/donate" or clean_text == "💸 Donate / Support":
            self.send_message(chat_id, RESPONSES["donate"], reply_markup=VISITOR_KEYBOARD)
            return

        # Regular query: send auto-responder if offline, and forward to Admin
        if not self.is_online:
            client_info = self.data["clients"].get(str(chat_id), {})
            last_reply = client_info.get("last_auto_reply", 0)
            # Only send auto-reply once every 10 minutes to avoid spamming the user
            if time.time() - last_reply > 600:
                self.send_message(chat_id, RESPONSES["welcome_offline"], reply_markup=VISITOR_KEYBOARD)
                client_info["last_auto_reply"] = time.time()
                self.data["clients"][str(chat_id)] = client_info
                self.save_json(DATA_FILE, self.data)

        # Forward message to Admin
        if self.admin_id:
            header = (
                f"📥 *Incoming Support Query*\n"
                f"👤 *From:* {first_name} (@{username or 'None'})\n"
                f"🆔 *ID:* `{chat_id}`\n"
                f"💬 *Query:*\n"
                f"\"{text}\"\n\n"
                f"✍️ *Reply to this message directly to respond.*"
            )
            fwd = self.send_message(self.admin_id, header)
            if fwd and fwd.get("ok"):
                fwd_msg_id = str(fwd["result"]["message_id"])
                # Map this forwarded message id to the client's chat id
                self.data["mappings"][fwd_msg_id] = chat_id
                self.save_json(DATA_FILE, self.data)
        else:
            self.send_message(chat_id, "⚠️ Support is temporarily offline (Setup in progress). The developer will register this endpoint shortly.")

    def run(self):
        if not self.token or self.token == "YOUR_TELEGRAM_BOT_TOKEN":
            print("[!] Cannot start bot. Please configure bot_config.json.")
            return

        print("[*] Long-polling started. Listening for messages...")
        offset = 0
        
        while True:
            try:
                updates = self.api_call("getUpdates", {"offset": offset, "timeout": 20})
                if updates and updates.get("ok"):
                    for update in updates.get("result", []):
                        offset = update["update_id"] + 1
                        message = update.get("message")
                        if not message:
                            continue
                            
                        chat = message.get("chat", {})
                        chat_id = chat.get("id")
                        text = message.get("text", "")
                        
                        first_name = chat.get("first_name", "Anonymous")
                        username = chat.get("username", "")

                        # Determine if message is from Admin or Client
                        if chat_id == self.admin_id:
                            if text.startswith("/"):
                                self.handle_admin_command(text, message.get("message_id"), chat_id)
                            else:
                                self.handle_admin_reply(message)
                        else:
                            # Registration process for admin
                            param = text[len("/start"):].strip()
                            if text.startswith("/start") and param == self.passcode:
                                self.admin_id = chat_id
                                self.send_message(self.admin_id, f"✅ Admin registered successfully! ID: {self.admin_id}\n\n*Available Commands:*\n• /online - Go online (turn off auto-responder)\n• /offline - Go offline (enable auto-responder)\n• /status - Check status")
                                self.save_config()
                            else:
                                self.handle_client_message(message, chat_id, first_name, username)
                                
            except KeyboardInterrupt:
                print("\n[*] Bot stopped by operator.")
                break
            except Exception as e:
                print(f"[!] Error in polling loop: {e}")
                time.sleep(5)

if __name__ == "__main__":
    bot = AetherSupportBot()
    bot.run()
