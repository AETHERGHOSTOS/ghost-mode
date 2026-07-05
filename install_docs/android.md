# Aether Ghost OS — Android Installation Guide (Termux)

Follow this step-by-step guide to run Aether Ghost OS on any Android device without root.

## 🛠️ Step 1: Install Termux
Do NOT download Termux from the Google Play Store (it is outdated and deprecated).
1. Download **F-Droid** or go to the [Termux F-Droid page](https://f-droid.org/en/packages/com.termux/).
2. Download and install the latest Termux APK.

## 📦 Step 2: Install Ghost OS
Open Termux and run the universal installation script:
```bash
curl -sL https://raw.githubusercontent.com/YOURUSERNAME/aether-ghost-os/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
```

## 🎥 Step 3: Grant Logcat Permissions (Camera & Mic Scan)
To allow the threat scanner to detect when other apps (like WhatsApp, Zoom, or Spyware) are using your microphone and camera without requiring root access:
1. Enable **USB Debugging** on your phone (under Developer Options).
2. Connect your phone to your PC.
3. Run the following command from your PC terminal (via ADB):
   ```bash
   adb shell pm grant com.termux android.permission.READ_LOGS
   ```
4. Restart Termux. Now Aether Ghost OS will scan hardware nodes dynamically!

## 👻 Step 4: Launching Aether
Launch the interactive CLI menu:
```bash
bash ~/ghost.sh
```
To access the Security Dashboard:
1. Select option `[5] 🖥️  Open Dashboard`.
2. Open your phone browser and go to: `http://localhost:8080/ghost_dashboard.html`.
