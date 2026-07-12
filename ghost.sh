#!/bin/bash
# 💀 AETHER GHOST OS LAUNCHER CONTROL v1.2.0

VERSION="1.2.0"

# Auto-start background server daemon if not running
if ! pgrep -f server_daemon.py >/dev/null; then
  for path in "$HOME/ghost_tools/server_daemon.py" "./ghost_tools/server_daemon.py"; do
    if [ -f "$path" ]; then
      python3 "$path" >/dev/null 2>&1 &
      sleep 1
      break
    fi
  done
fi

while true; do
  clear

  # Try to render logo
  for path in "$HOME/ghost_tools/render_logo.py" "./ghost_tools/render_logo.py"; do
    if [ -f "$path" ]; then
      python3 "$path" 2>/dev/null
      break
    fi
  done

  echo ""
  echo "  👻 A E T H E R   G H O S T   O S  v${VERSION} 👻"
  echo "  ============================================="
  echo "  Privacy Operating Security Suite for Termux"
  echo ""
  echo -e "  \e[1;32m[1]\e[0m 👻 Select Anonymity Engine"
  echo -e "  \e[1;32m[2]\e[0m 🛡️ AetherGhost Guard Scans"
  echo -e "  \e[1;32m[3]\e[0m 💀 Run Full System Security Audit"
  echo -e "  \e[1;32m[4]\e[0m 🌍 Pick Tor Location Node"
  echo -e "  \e[1;32m[5]\e[0m 🌐 Check My Connection"
  echo -e "  \e[1;32m[6]\e[0m 🖥️  Open Dashboard"
  echo -e "  \e[1;32m[7]\e[0m 📋 View System Logs"
  echo -e "  \e[1;32m[8]\e[0m 🔧 Change DNS Resolver"
  echo -e "  \e[1;32m[9]\e[0m 🚨 PANIC — Self Destruct"
  echo -e "  \e[1;32m[10]\e[0m ⏹️  Stop Everything & Exit"
  echo -e "  \e[1;32m[12]\e[0m 🚪 Exit Menu (Keep Services Running)"
  echo -e "  \e[1;32m[13]\e[0m 🔄 Check & Pull Updates"
  echo -e "  \e[1;32m[14]\e[0m 🤖 Telegram Sentry Bot Setup"
  echo -e "  \e[1;32m[0]\e[0m 🔤 Reset Termux Font"
  echo -e "  \e[1;32m[11]\e[0m ☕ Support & Donate to Project"
  echo ""
  read -p "  Choose [0-14]: " c
  echo ""

  case $c in
    1)
      echo "  😈 SELECT ANONYMITY ENGINE:"
      echo "  ----------------------------"
      echo "  [1] 😈 Tor Proxy Network"
      echo "  [2] 🌐 Cloudflare WARP VPN"
      echo "  [3] 🌍 Public SOCKS5 Proxy Rotation"
      echo "  [4] 🛡️  Secure DNS-over-HTTPS (DoH)"
      echo "  [5] ⚠️  No Anonymity (UNPROTECTED!)"
      echo ""
      read -p "  Select [1-5]: " eng_c

      CFG="$HOME/ghost_tools/schedule_config.json"
      mkdir -p "$HOME/ghost_tools"

      case $eng_c in
        1)
          echo "😈 Activating Tor Proxy..."
          pkill tor 2>/dev/null; sleep 1
          tor > /dev/null 2>&1 &
          python3 -c "
import json, os
p = os.path.expanduser('~/ghost_tools/schedule_config.json')
c = json.load(open(p)) if os.path.exists(p) else {}
c['anonymity_engine'] = 'tor'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null
          echo "⏳ Warming up Tor circuits (15 seconds)..."
          sleep 15
          ANON=$(curl -s --max-time 10 --socks5-hostname 127.0.0.1:9050 https://icanhazip.com 2>/dev/null)
          REAL=$(curl -s --max-time 5 https://icanhazip.com)
          if [ -n "$ANON" ] && [ "$ANON" != "$REAL" ]; then
            echo -e "💀 \e[1;32m[ GHOST ACTIVE ]\e[0m Anonymous IP: $ANON"
          else
            echo "⏳ Tor still bootstrapping. Check option 4 in a moment."
          fi
          ;;
        2)
          echo "🌐 Activating Cloudflare WARP VPN..."
          pkill tor 2>/dev/null
          warp-cli connect 2>/dev/null || echo "⚠️  WARP not installed. Install: pkg install cloudflare-warp"
          python3 -c "
import json, os
p = os.path.expanduser('~/ghost_tools/schedule_config.json')
c = json.load(open(p)) if os.path.exists(p) else {}
c['anonymity_engine'] = 'warp'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null
          ;;
        3)
          echo "🌍 SOCKS5 Proxy Rotation selected."
          pkill tor 2>/dev/null
          python3 -c "
import json, os
p = os.path.expanduser('~/ghost_tools/schedule_config.json')
c = json.load(open(p)) if os.path.exists(p) else {}
c['anonymity_engine'] = 'proxy'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null
          ;;
        4)
          echo "🛡️  Activating DNS-over-HTTPS..."
          pkill tor 2>/dev/null
          python3 -c "
import json, os
p = os.path.expanduser('~/ghost_tools/schedule_config.json')
c = json.load(open(p)) if os.path.exists(p) else {}
c['anonymity_engine'] = 'doh'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null
          echo "✅ DoH active — DNS queries encrypted."
          echo "   Your IP is NOT hidden. Only DNS is encrypted."
          ;;
        5)
          echo "⚠️  WARNING: Disabling anonymity. Your real IP will be exposed."
          pkill tor 2>/dev/null
          warp-cli disconnect 2>/dev/null
          python3 -c "
import json, os
p = os.path.expanduser('~/ghost_tools/schedule_config.json')
c = json.load(open(p)) if os.path.exists(p) else {}
c['anonymity_engine'] = 'none'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null
          echo "⚠️  Anonymity disabled. Connection is now UNPROTECTED."
          ;;
        *)
          echo "Invalid choice."
          ;;
      esac
      ;;

    2)
      echo "  🛡️ AETHERGHOST GUARD SCAN CENTER:"
      echo "  ---------------------------------"
      echo "  [1] 🦠 Scan Active Memory (Virus Guard)"
      echo "  [2] 💾 Scan Storage Files (Malware Guard)"
      echo ""
      read -p "  Select [1-2]: " scan_c
      SCRIPT=$(find "$HOME" ./  -name "ghost_mode.py" 2>/dev/null | head -1)
      if [ -n "$SCRIPT" ]; then
        case $scan_c in
          1)
            python3 "$SCRIPT" --virus
            ;;
          2)
            python3 "$SCRIPT" --malware
            ;;
          *)
            echo "Invalid choice."
            ;;
        esac
      else
        echo "❌ ghost_mode.py not found."
      fi
      ;;

    3)
      SCRIPT=$(find "$HOME" ./ -name "ghost_mode.py" 2>/dev/null | head -1)
      if [ -n "$SCRIPT" ]; then
        python3 "$SCRIPT"
      else
        echo "❌ ghost_mode.py not found."
      fi
      ;;

    4)
      PICKER=$(find "$HOME/ghost_tools" ./ -name "location_picker.py" 2>/dev/null | head -1)
      if [ -n "$PICKER" ]; then
        python3 "$PICKER"
      else
        echo "❌ location_picker.py not found."
      fi
      ;;

    5)
      # Check connection status
      CFG="$HOME/ghost_tools/schedule_config.json"
      ENG="tor"
      if [ -f "$CFG" ]; then
        ENG=$(python3 -c "import json; print(json.load(open('$CFG')).get('anonymity_engine','tor'))" 2>/dev/null)
      fi

      echo "🔒 Active Engine: ${ENG^^}"
      REAL=$(curl -s --max-time 5 https://icanhazip.com)
      echo "🌐 Your Real IP:  $REAL"

      if [ "$ENG" = "tor" ]; then
        ANON=$(curl -s --max-time 10 --socks5-hostname 127.0.0.1:9050 https://icanhazip.com 2>/dev/null)
        if [ -n "$ANON" ] && [ "$ANON" != "$REAL" ]; then
          echo -e "💀 \e[1;32m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m 👻"
           echo "🕵️ Tor Anonymous IP: $ANON"
           echo ""
           echo "🔍 To verify full anonymity or route your browser:"
           echo "   → Install Orbot app → enable VPN mode, then visit check.torproject.org"
           echo "   → Or manually set your browser SOCKS5 proxy to: 127.0.0.1:9050"
           echo ""
           echo -e "  \e[0;36m🚀 COMING SOON FROM AETHER:\e[0m"
           echo "   📱 Aether Mobile App — protect every app on your phone"
           echo "   🔒 Aether VPN     — full-device encrypted tunnel"
           echo "   🌍 Aether Proxy   — rotating SOCKS5 proxy network"
           echo "   🌐 Aether Browser — private, proxy-integrated browser"
        else
          echo "⚠️  Tor not masking IP yet. Wait 15 seconds and try again."
        fi
      elif [ "$ENG" = "warp" ]; then
        TRACE=$(curl -s --max-time 5 https://www.cloudflare.com/cdn-cgi/trace)
        if echo "$TRACE" | grep -q "warp=on"; then
          echo -e "💀 \e[1;32m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m 👻 (WARP connected)"
        else
          echo "⚠️  WARP disconnected."
        fi
      elif [ "$ENG" = "doh" ]; then
        echo "🛡️  DoH active — DNS encrypted. IP not hidden."
      elif [ "$ENG" = "none" ]; then
        echo -e "⚠️  \e[1;31mUNPROTECTED — Enable an engine!\e[0m"
      fi
      ;;

    6)
      # Open dashboard
      if ! pgrep -f server_daemon.py >/dev/null; then
        echo "🖥️  Starting dashboard server..."
        DAEMON=$(find "$HOME/ghost_tools" ./ -name "server_daemon.py" 2>/dev/null | head -1)
        if [ -n "$DAEMON" ]; then
          python3 "$DAEMON" >/dev/null 2>&1 &
          sleep 2
        fi
      fi
      echo "🌐 Dashboard: http://localhost:8080/ghost_dashboard.html"
      termux-open "http://localhost:8080/ghost_dashboard.html" 2>/dev/null || \
        echo "Open in browser: http://localhost:8080/ghost_dashboard.html"
      ;;

    7)
      echo "📋 Last 40 log lines:"
      echo "---------------------"
      LOG_FILE="$HOME/ghost_tools/ghost.log"
      if [ -f "$LOG_FILE" ]; then
        tail -40 "$LOG_FILE"
      else
        echo "No logs yet. Run a scan first (option 1)."
      fi
      ;;

    8)
      # DNS Changer
      SCRIPT=$(find "$HOME" ./ -name "ghost_mode.py" 2>/dev/null | head -1)
      if [ -n "$SCRIPT" ]; then
        python3 "$SCRIPT" --dns
      else
        echo "❌ ghost_mode.py not found."
      fi
      ;;

    9)
      echo "🚨 PANIC MODE — Self-destruct security profiles..."
      read -p "🚨 Are you sure you want to proceed? (y/n): " confirm
      if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        SCRIPT=$(find "$HOME" ./ -name "ghost_mode.py" 2>/dev/null | head -1)
        if [ -n "$SCRIPT" ]; then
          python3 "$SCRIPT" --panic
        fi
      else
        echo "Panic cancelled."
      fi
      ;;

    10)
      echo "⏹️  Stopping Aether Ghost OS..."
      pkill tor 2>/dev/null && echo "✅ Tor stopped"
      warp-cli disconnect 2>/dev/null
      pkill -f server_daemon.py 2>/dev/null && echo "✅ Dashboard server stopped"
      pkill crond 2>/dev/null && echo "✅ Auto-scan stopped"
      echo "🤫 Ghost Mode deactivated."
      break
      ;;

    0)
      rm -f ~/.termux/font.ttf
      termux-reload-settings 2>/dev/null
      echo "✅ Font reset to system default."
      ;;

    11)
      echo "=========================================================="
      echo "  ☕ SUPPORT AETHER GHOST OS DEVELOPMENT"
      echo "=========================================================="
      echo "  If this tool keeps you secure, consider supporting us!"
      echo ""
      echo "  🌐 Web Donations:"
      echo "     Buy Me a Coffee: https://buymeacoffee.com/aetherghost.os"
      echo ""
      echo "  🪙 Crypto Addresses:"
      echo "     USDT  | TRX - Tron (TRC20):           TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU"
      echo "     USDC  | SOL - Solana:                 9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui"
      echo "     USDT  | ETH - Ethereum (ERC20):       0x09cad574c2c39a88ce931307361682680b795490"
      echo "     BNB   | BSC - BNB Smart Chain (BEP20): 0x09cad574c2c39a88ce931307361682680b795490"
      echo "     BNB   | ETH - Ethereum (ERC20):       0x09cad574c2c39a88ce931307361682680b795490"
      echo "     BTC   | BTC - Bitcoin (Native):        15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k"
      echo "     BTC   | SEGWIT - BTC (SegWit):        bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj"
      echo "     WBTC  | BSC - BNB Smart Chain (BEP20): 0x09cad574c2c39a88ce931307361682680b795490"
      echo "     WBTC  | ETH - Ethereum (ERC20):       0x09cad574c2c39a88ce931307361682680b795490"
      echo ""
      echo "  ⚠️  IMPORTANT: Native Bitcoin (BTC) ONLY goes to the Native/SegWit addresses."
      echo "     Sending real BTC to an EVM address will permanently lose your funds."
      echo ""
      echo "  Thank you for keeping Aether Ghost OS active and secure!"
      echo "=========================================================="
      ;;

    13)
      if [ ! -d ".git" ]; then
        echo "ℹ️ Installed via ZIP — git repository not found."
        echo "   To update, download the latest ZIP from: https://github.com/AETHERGHOSTOS/ghost-mode"
      else
        echo "🔄 Checking for updates from GitHub..."
        git fetch && git status
        if git status -uno | grep -q "behind"; then
          read -p "💡 New update detected! Pull latest code changes? (y/n): " pull_choice
          if [[ "$pull_choice" == "y" || "$pull_choice" == "Y" ]]; then
            git pull
            echo "✅ Update complete! Restaging launcher..."
            sleep 2
          fi
        else
          echo "🟢 System is already up-to-date!"
        fi
      fi
      ;;

    14)
      python3 -c "import sys; sys.path.append('.'); from ghost_mode import print_sentry_status; print_sentry_status()"
      ;;

    12)
      echo "🚪 Exiting menu. Background Sentry and Anonymity daemon remains ACTIVE."
      echo "🌐 Dashboard is online: http://localhost:8080/ghost_dashboard.html"
      echo ""
      break
      ;;

    *)
      echo "Invalid choice."
      ;;
  esac

  echo ""
  read -p "Press [Enter] to return to menu..."
done
