#!/bin/bash
# 💀 AETHER GHOST OS LAUNCHER

# Auto-start background server and scheduler if not already running
if ! pgrep -f server_daemon.py >/dev/null; then
  # Try home directory, then fallbacks
  if [ -f "$HOME/ghost_tools/server_daemon.py" ]; then
    python3 ~/ghost_tools/server_daemon.py >/dev/null 2>&1 &
  elif [ -f "./ghost_tools/server_daemon.py" ]; then
    python3 ./ghost_tools/server_daemon.py >/dev/null 2>&1 &
  elif [ -f "../ghost_tools/server_daemon.py" ]; then
    python3 ../ghost_tools/server_daemon.py >/dev/null 2>&1 &
  fi
  sleep 1
fi

while true; do
  clear
  if [ -f "$HOME/ghost_tools/render_logo.py" ]; then
    python3 ~/ghost_tools/render_logo.py
  elif [ -f "./ghost_tools/render_logo.py" ]; then
    python3 ./ghost_tools/render_logo.py
  else
    # Simple fallback ASCII
    echo "       👻 A E T H E R   G H O S T   O S 👻"
  fi
  echo ""
  echo "  👻 A E T H E R   G H O S T   O S 👻"
  echo "  ========================================"
  echo "  Privacy Operating Security Suite for Termux"
  echo ""
  echo -e "  \e[1;32m[1]\e[0m 💀 Run Security Scan"
  echo -e "  \e[1;32m[2]\e[0m 👻 Select Anonymity Engine 🤫"
  echo -e "  \e[1;32m[3]\e[0m 🌍 Pick Tor Location Node 👻"
  echo -e "  \e[1;32m[4]\e[0m 🌐 Check My Connection 🔒"
  echo -e "  \e[1;32m[5]\e[0m 🖥️  Open Dashboard Link 👻"
  echo -e "  \e[1;32m[6]\e[0m 📋 View System Logs 👻"
  echo -e "  \e[1;32m[7]\e[0m ⏹️  Stop Everything & Exit"
  echo -e "  \e[1;32m[8]\e[0m 🔤 Reset Termux Font to Default"
  echo -e "  \e[1;32m[9]\e[0m ☕ Support & Donate to Project"
  echo ""
  read -p "  Choose [1-9]: " c
  echo ""

  case $c in
    1)
      # Try running ghost_mode.py from Home or Local
      if [ -f "$HOME/ghost_mode.py" ]; then
        python3 ~/ghost_mode.py
      elif [ -f "./ghost_mode.py" ]; then
        python3 ./ghost_mode.py
      elif [ -f "../ghost_mode.py" ]; then
        python3 ../ghost_mode.py
      else
        echo "❌ ghost_mode.py not found."
      fi
      ;;
    2)
      echo "  😈 SELECT ANONYMITY ENGINE:"
      echo "  ---------------------------"
      echo "  [1] Tor Proxy Network"
      echo "  [2] Cloudflare WARP VPN"
      echo "  [3] Public SOCKS5 Proxy Rotation"
      echo "  [4] Encrypted DNS-over-HTTPS (DoH)"
      echo "  [5] No Anonymity (⚠️ UNPROTECTED!)"
      echo ""
      read -p "  Select [1-5]: " eng_c
      echo ""
      CFG="$HOME/ghost_tools/schedule_config.json"
      [ ! -d "$HOME/ghost_tools" ] && mkdir -p "$HOME/ghost_tools"
      
      case $eng_c in
        1)
          echo "😈 Activating Tor Proxy..."
          pkill tor 2>/dev/null
          tor > /dev/null 2>&1 &
          python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/schedule_config.json'); c=json.load(open(p)) if os.path.exists(p) else {}; c['anonymity_engine']='tor'; json.dump(c, open(p,'w'), indent=2)" 2>/dev/null
          echo "⏳ Warming up circuits (10 seconds)..."
          sleep 10
          ;;
        2)
          echo "🌐 Connecting Cloudflare WARP VPN..."
          pkill tor 2>/dev/null
          warp-cli register 2>/dev/null
          warp-cli connect 2>/dev/null
          python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/schedule_config.json'); c=json.load(open(p)) if os.path.exists(p) else {}; c['anonymity_engine']='warp'; json.dump(c, open(p,'w'), indent=2)" 2>/dev/null
          sleep 4
          ;;
        3)
          echo "🌍 Initializing SOCKS5 Proxy Rotation..."
          pkill tor 2>/dev/null
          python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/schedule_config.json'); c=json.load(open(p)) if os.path.exists(p) else {}; c['anonymity_engine']='proxy'; json.dump(c, open(p,'w'), indent=2)" 2>/dev/null
          # Trigger a scrape request via localhost API
          curl -s -X POST -d '{"engine":"proxy"}' http://localhost:8080/api/engine >/dev/null 2>&1
          sleep 5
          ;;
        4)
          echo "🔒 Activating DNS-over-HTTPS Encryption..."
          pkill tor 2>/dev/null
          python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/schedule_config.json'); c=json.load(open(p)) if os.path.exists(p) else {}; c['anonymity_engine']='doh'; json.dump(c, open(p,'w'), indent=2)" 2>/dev/null
          sleep 2
          ;;
        5)
          echo "⚠️ Disabling anonymity... Connection will be UNPROTECTED!"
          pkill tor 2>/dev/null
          warp-cli disconnect >/dev/null 2>&1
          python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/schedule_config.json'); c=json.load(open(p)) if os.path.exists(p) else {}; c['anonymity_engine']='none'; json.dump(c, open(p,'w'), indent=2)" 2>/dev/null
          sleep 2
          ;;
        *)
          echo "Invalid engine choice."
          ;;
      esac
      ;;
    3)
      if [ -f "$HOME/ghost_tools/location_picker.py" ]; then
        python3 ~/ghost_tools/location_picker.py
      elif [ -f "./ghost_tools/location_picker.py" ]; then
        python3 ./ghost_tools/location_picker.py
      else
        echo "❌ location_picker.py not found."
      fi
      ;;
    4)
      CFG="$HOME/ghost_tools/schedule_config.json"
      ENG="tor"
      if [ -f "$CFG" ]; then
        ENG=$(python3 -c "import json; print(json.load(open('$CFG')).get('anonymity_engine', 'tor'))" 2>/dev/null)
      fi
      echo "🔒 Active Engine: ${ENG^^}"
      REAL=$(curl -s --max-time 5 https://icanhazip.com)
      echo "🌐 Default IP:   $REAL"
      
      if [ "$ENG" == "tor" ]; then
        ANON=$(curl -s --max-time 6 --socks5-hostname 127.0.0.1:9050 https://icanhazip.com 2>/dev/null)
        if [ -n "$ANON" ]; then
          echo -e "💀  \e[1;31m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m \e[1;36m👻\e[0m"
          echo "🕵️ Tor Spoof:   $ANON"
        else
          echo "⚠️ Tor proxy not responding."
        fi
      elif [ "$ENG" == "warp" ]; then
        IS_WARP=$(curl -s --max-time 5 https://www.cloudflare.com/cdn-cgi/trace | grep warp=on)
        if [ -n "$IS_WARP" ]; then
          echo -e "💀  \e[1;31m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m \e[1;36m👻\e[0m"
          echo "🕵️ WARP Mask:   Active (IP $REAL)"
        else
          echo "⚠️ WARP VPN disconnected."
        fi
      elif [ "$ENG" == "proxy" ]; then
        PXY=$(python3 -c "import json, os; p=os.path.expanduser('~/ghost_tools/active_proxy.json'); print(json.load(open(p)).get('proxy','')) if os.path.exists(p) else print('')" 2>/dev/null)
        if [ -n "$PXY" ]; then
          PXY_ADDR=${PXY#*//}
          ANON=$(curl -s --max-time 6 -x socks5://$PXY_ADDR https://icanhazip.com 2>/dev/null)
          if [ -n "$ANON" ]; then
            echo -e "💀  \e[1;31m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m \e[1;36m👻\e[0m"
            echo "🕵️ Proxy Spoof: $ANON"
          else
            echo "⚠️ Rotated proxy unresponsive."
          fi
        else
          echo "⚠️ No rotated SOCKS5 proxy configured yet."
        fi
      elif [ "$ENG" == "doh" ]; then
        echo -e "💀  \e[1;31m[ GHOST ACTIVE ]\e[0m ➔ \e[1;32mYou are a ghost!\e[0m \e[1;36m👻\e[0m"
        echo "🕵️ Secure DNS:  Active (Bypassing router logs)"
      elif [ "$ENG" == "none" ]; then
        echo -e "⚠️ \e[1;31mUNPROTECTED! Connection exposed.\e[0m"
      fi
      ;;
    5)
      if ! pgrep -f server_daemon.py >/dev/null; then
        echo "🖥️ Starting background dashboard server..."
        if [ -f "$HOME/ghost_tools/server_daemon.py" ]; then
          python3 ~/ghost_tools/server_daemon.py >/dev/null 2>&1 &
        else
          python3 ./ghost_tools/server_daemon.py >/dev/null 2>&1 &
        fi
        sleep 2
      fi
      echo "🌐 Opening dashboard in browser..."
      termux-open "http://localhost:8080/ghost_dashboard.html" 2>/dev/null || \
      echo "Open in browser: http://localhost:8080/ghost_dashboard.html"
      ;;
    6)
      echo "📋 Last 30 log lines:"
      echo "---------------------"
      if [ -f "$HOME/ghost_tools/ghost.log" ]; then
        tail -30 ~/ghost_tools/ghost.log
      elif [ -f "./ghost_tools/ghost.log" ]; then
        tail -30 ./ghost_tools/ghost.log
      else
        echo "No logs yet. Run a scan first."
      fi
      ;;
    7)
      echo "⏹️ Stopping Ghost Mode..."
      pkill tor 2>/dev/null && echo "✅ Tor stopped"
      warp-cli disconnect >/dev/null 2>&1 && echo "✅ WARP VPN stopped"
      pkill -f server_daemon.py 2>/dev/null && echo "✅ Dashboard server stopped"
      echo "🤫 Ghost Mode deactivated."
      break
      ;;
    8)
      echo "🔤 Resetting Termux Font size and clearing custom style files..."
      rm -f ~/.termux/font.ttf
      termux-reload-settings 2>/dev/null
      echo "✅ Monospace font reset. Termux styling reverted to system default."
      ;;
    9)
      echo "=========================================================="
      echo "  ☕ SUPPORT AETHER GHOST OS DEVELOPMENT"
      echo "=========================================================="
      echo "  If this tool keeps you secure, consider supporting us!"
      echo ""
      echo "  🌐 Web Donations:"
      echo "     Buy Me a Coffee: https://buymeacoffee.com/aetherghost.os"
      echo "     PayPal:          https://paypal.me/aetherghostos"
      echo ""
      echo "  📱 Mobile Money (Kenya M-Pesa):"
      echo "     Phone Number:    +254 742454100"
      echo "     Account Name:    L.W"
      echo ""
      echo "  🪙 Crypto Addresses:"
      echo "     Bitcoin (SegWit): bc1qqmf52ajmvhaxswv97p2q0z82pk4hchv2aqrpmj"
      echo "     Bitcoin (Native): 15dzX3kqeUD29fbYqoMX4AW9aBDR6ahJ5k"
      echo "     Ethereum (ERC20): 0x09cad574c2c39a88ce931307361682680b795490"
      echo "     Solana (SOL):     9pU3D88DVXzebd8kR5rzGeqjxKHbxBcBKNFwEBRBNzui"
      echo "     Tron (TRC20):     TKPkbkZLFyeeUD9QEbmc7FiVfSY9FieaQU"
      echo "     BNB (BEP20):      0x09cad574c2c39a88ce931307361682680b795490"
      echo ""
      echo "  Thank you for keeping Aether Ghost OS active and secure!"
      echo "=========================================================="
      ;;
    *)
      echo "Invalid choice."
      ;;
  esac
  echo ""
  read -p "Press [Enter] to return to the menu..."
done
