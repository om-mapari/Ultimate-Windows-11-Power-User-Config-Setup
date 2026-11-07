# Omiflix (Jellyfin) Setup & Backup Documentation

This directory contains the complete backup of Om's **Omiflix** (customized Jellyfin Media Server) configuration, custom scripts, plugins, branding, and startup behavior.

---

## Directory Structure

### 🚀 launcher/
- launch-jellyfin.vbs - Smart on-demand background launcher. Checks if jellyfin.exe is already running; if not, starts the tray/server silently, waits for HTTP 200 on port 8096, and opens the Brave Web App (--app="http://jellyfin.local:8096").
- Omiflix.lnk - Preconfigured Start Menu shortcut pointing to wscript.exe "%USERPROFILE%\launch-jellyfin.vbs" with the custom borderless omiflix.ico icon.
- omiflix.ico - Multi-resolution Windows icon (256x256 down to 16x16) with transparent squircle borders.
- omiflix-clean.png - High-resolution master transparent PNG for the app icon.

### 🎨 randing/
- omiflix-logo.svg - Mathematically warped vector logo of **OMIFLIX** in Bebas Neue font featuring the signature Netflix curved bottom arch and flat top.
- omiflix-clean.png - Borderless, transparent squircle app icon.
- new-icon.png - Source icon art provided by user.
- ebas.ttf - Bebas Neue font file used to generate the vector wordmark.
- generate_logo.py - Python script that generates the warped curved SVG path using onttools.
- pply_curved_logo.py - Script that encodes the SVG into a data URI and applies it to Jellyfin's randing.xml.

### ⚙️ server-config/
- randing.xml - Core visual branding configuration containing the full custom CSS:
  - Netflin theme import (hza-code/Netflin@latest).
  - Media covers add-on (media-covers.min.css).
  - Lucide icons & metadata icons.
  - Custom vector **OMIFLIX** curved wordmark data URI.
  - Navigation button cleaner (utton[title="Back"], button[title="Forward"] { display: none !important; }).
  - Border radius customization (--nf-radius: 12px).
- system.xml - Server configuration including:
  - <ServerName>Omiflix</ServerName> (rebranded server title for window & tab headers).
  - Custom plugin repositories list:
    1. Jellyfin Stable: https://repo.jellyfin.org/files/plugin/manifest.json
    2. Jellyfin Player Queue: https://raw.githubusercontent.com/k1k4k/jellyfin-player-queue/main/manifest.json
    3. Jellyfin Enhanced / JS Injector (v12): https://raw.githubusercontent.com/n00bcodr/jellyfin-plugins/main/12/manifest.json
    4. File Transformation: https://www.iamparadox.dev/jellyfin/plugins/manifest.json
- 
etwork.xml - Network and port bindings.
- ncoding.xml - Transcoding configurations.

### 🧩 plugins/configurations/
- Jellyfin.Plugin.JavaScriptInjector.xml - Injected script configuration including the "Hide Player Controls (G Key)" script.
- Jellyfin.Plugin.JellyfinEnhanced.xml - Complete configuration for ratings badges, TMDB/IMDB/RottenTomatoes integrations, pause screen overlays, spoiler guards.
- Jellyfin.Plugin.FileTransformation.xml - Prerequisite dependency for web transformations.
- Jellyfin.Plugin.QueueOsd.xml - Player queue overlay controls.
- Jellyfin.Plugin.OpenSubtitles.xml - Subtitles downloader plugin config.
- Subfolders: Jellyfin.Plugin.JellyfinEnhanced/, Jellyfin.Plugin.PluginPages/.

### 📜 scripts/
- hide-controls.js - Standalone JavaScript / UserScript code for the 'G' key shortcut (toggles visibility of OSD, top header, pause screen overlay, queue, but keeps cursor visible).

---

## Auto-Start Policy
- JellyfinTray was removed from HKCU:\Software\Microsoft\Windows\CurrentVersion\Run.
- Jellyfin does **NOT** run on Windows startup; it starts exclusively on-demand when the user clicks the Omiflix shortcut.

---

## Future Restore Procedure (New PC / Fresh Install)

1. **Launcher & Shortcut:**
   - Copy launcher\launch-jellyfin.vbs to %USERPROFILE%\launch-jellyfin.vbs.
   - Copy launcher\omiflix.ico to %USERPROFILE%\omiflix.ico.
   - Copy launcher\Omiflix.lnk to %APPDATA%\Microsoft\Windows\Start Menu\Programs\Omiflix.lnk.

2. **Disable Auto-Start on Boot:**
   - Ensure JellyfinTray is deleted from HKCU:\Software\Microsoft\Windows\CurrentVersion\Run.

3. **Restore Server Settings & Branding:**
   - Copy server-config\branding.xml to %ProgramData%\Jellyfin\Server\config\branding.xml.
   - Copy server-config\system.xml to %ProgramData%\Jellyfin\Server\config\system.xml.
   - Copy server-config\network.xml to %ProgramData%\Jellyfin\Server\config\network.xml.
   - Copy server-config\encoding.xml to %ProgramData%\Jellyfin\Server\config\encoding.xml.

4. **Install Plugins:**
   - Add the 4 plugin repository URLs from server-config\system.xml into Dashboard -> Plugins -> Repositories.
   - Install from Catalog: Jellyfin Enhanced, JavaScript Injector, File Transformation, Jellyfin Player Queue, Open Subtitles.
   - Copy all XMLs from plugins\configurations\ to %ProgramData%\Jellyfin\Server\plugins\configurations\.

5. **Restart Jellyfin & Hard Refresh Client:**
   - Restart the server.
   - Press Ctrl + F5 on the web app to load the new curved **OMIFLIX** branding.

