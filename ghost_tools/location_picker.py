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
    # Read existing torrc
    lines = []
    try:
        with open(TORRC) as f:
            lines = [l for l in f.readlines()
                     if "ExitNodes" not in l and "StrictNodes" not in l]
    except:
        pass

    if codes:
        country_str = ",".join([f"{{{c}}}" for c in codes])
        lines.append(f"\nExitNodes {country_str}\n")
        lines.append("StrictNodes 1\n")
        print(f"\n✅ Tor exit set to: {country_str}")
    else:
        print("\n✅ Random location mode — Tor picks automatically")

    with open(TORRC, "w") as f:
        f.writelines(lines)

    # Restart Tor
    print("🔄 Restarting Tor...")
    subprocess.run("pkill tor 2>/dev/null", shell=True)
    import time; time.sleep(2)
    subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
