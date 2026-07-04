#!/usr/bin/env python3
"""
😈 GHOST LOCATION PICKER
=========================
Pick one or multiple Tor exit countries.
Your traffic will appear to come from there.
"""

import subprocess, os

TORRC = os.path.expanduser("~/../usr/etc/tor/torrc")

LOCATIONS = {
    "1":  ("🇺🇸 United States",    "US"),
    "2":  ("🇬🇧 United Kingdom",    "GB"),
    "3":  ("🇩🇪 Germany",           "DE"),
    "4":  ("🇳🇱 Netherlands",       "NL"),
    "5":  ("🇫🇷 France",            "FR"),
    "6":  ("🇨🇭 Switzerland",       "CH"),
    "7":  ("🇸🇪 Sweden",            "SE"),
    "8":  ("🇳🇴 Norway",            "NO"),
    "9":  ("🇯🇵 Japan",             "JP"),
    "10": ("🇨🇦 Canada",            "CA"),
    "11": ("🇦🇺 Australia",         "AU"),
    "12": ("🇧🇷 Brazil",            "BR"),
    "13": ("🇮🇳 India",             "IN"),
    "14": ("🇸🇬 Singapore",         "SG"),
    "15": ("🇿🇦 South Africa",      "ZA"),
    "16": ("🇷🇺 Russia",            "RU"),
    "17": ("🇺🇦 Ukraine",           "UA"),
    "18": ("🇵🇱 Poland",            "PL"),
    "19": ("🇦🇹 Austria",           "AT"),
    "20": ("🇷🇴 Romania",           "RO"),
    "0":  ("🌍 Random (auto)",      ""),
}

def show_menu():
    print()
    print("😈 AETHER GHOST OS LOCATION PICKER 💀")
    print("=" * 45)
    print("Pick where your traffic appears from:")
    print()
    for k, (name, code) in LOCATIONS.items():
        print(f"  [{k:>2}] {name}")
    print()

def apply_locations(codes):
    # Determine platform specific torrc path
    torrc_path = "/etc/tor/torrc" # default fallback
    termux_path = os.path.expanduser("~/../usr/etc/tor/torrc")
    
    if os.path.exists(termux_path) or "com.termux" in termux_path:
        torrc_path = termux_path
    elif os.path.exists("/etc/tor/torrc"):
        torrc_path = "/etc/tor/torrc"
    elif os.path.exists("/usr/local/etc/tor/torrc"):
        torrc_path = "/usr/local/etc/tor/torrc"
    else:
        # Custom or Windows path: local workspace file torrc
        torrc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "torrc")

    # Read existing torrc config lines
    lines = []
    if os.path.exists(torrc_path):
        try:
            with open(torrc_path, "r", encoding="utf-8") as f:
                lines = [l for l in f.readlines()
                         if "ExitNodes" not in l and "StrictNodes" not in l]
        except Exception as e:
            print(f"⚠️ Could not read Tor configuration: {e}")

    # Inject country nodes
    if codes:
        country_str = ",".join([f"{{{c}}}" for c in codes])
        lines.append(f"\nExitNodes {country_str}\n")
        lines.append("StrictNodes 1\n")
        print(f"\n✅ Tor exit set to: {country_str}")
    else:
        print("\n✅ Random location mode — Tor picks automatically")

    # Write changes safely
    try:
        os.makedirs(os.path.dirname(torrc_path), exist_ok=True)
        with open(torrc_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"✅ Tor configuration file updated: {torrc_path}")
    except Exception as e:
        print(f"⚠️ Permission denied: Could not write Tor settings file: {e}")

    # Restart Tor
    print("🔄 Restarting Tor...")
    if os.name == "nt":
        subprocess.run("taskkill /f /im tor.exe 2>nul", shell=True)
    else:
        subprocess.run("pkill tor 2>/dev/null", shell=True)
    import time; time.sleep(2)
    try:
        subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Could not start Tor daemon automatically: {e}")
    print("⏳ Waiting 15 seconds for Tor to bootstrap circuits...")
    time.sleep(15)

    # Check new IP with retries
    print("🌐 Getting your new anonymous IP...")
    ip = ""
    for attempt in range(1, 4):
        res = subprocess.run("curl -s --max-time 10 --socks5-hostname 127.0.0.1:9050 https://icanhazip.com", shell=True, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip() and not res.stdout.strip().startswith("curl:") and "<html" not in res.stdout.lower():
            ip = res.stdout.strip()
            break
        print(f"   (Attempt {attempt}/3: Tor circuit still building, retrying in 3s...)")
        time.sleep(3)
        
    loc = ""
    if ip:
        import json
        try:
            loc_cmd = f"curl -s --max-time 8 --socks5-hostname 127.0.0.1:9050 https://freeipapi.com/api/json/{ip}"
            loc_res = subprocess.run(loc_cmd, shell=True, capture_output=True, text=True)
            if loc_res.returncode == 0 and loc_res.stdout.strip():
                loc_data = json.loads(loc_res.stdout.strip())
                loc = loc_data.get("countryName", "Unknown")
        except:
            pass
        if not loc:
            loc = "Unknown Location"
            
        print(f"\n💀😈 AETHER GHOST OS ACTIVE")
        print(f"   Anonymous IP : {ip}")
        print(f"   Appears from : {loc}")
    else:
        print("\n⚠️  Tor still warming up or curl error. Wait 15 seconds then run:")
        print("   curl --socks5-hostname 127.0.0.1:9050 https://ifconfig.me")
    print()

def main():
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--apply":
        choice = sys.argv[2]
    else:
        show_menu()
        choice = input("Enter number(s) separated by comma [e.g. 1,3,5 or 0 for random]: ").strip()

    if not choice:
        print("No selection made.")
        return

    selected_codes = []
    parts = [p.strip() for p in choice.split(",")]

    for p in parts:
        if p in LOCATIONS:
            name, code = LOCATIONS[p]
            if code:
                selected_codes.append(code)
                print(f"  ✓ Selected: {name}")
            else:
                selected_codes = []  # random
                print("  ✓ Random location selected")
                break
        else:
            print(f"  ✗ '{p}' not valid, skipping")

    apply_locations(selected_codes)

if __name__ == "__main__":
    main()
