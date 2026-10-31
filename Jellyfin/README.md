# Jellyfin Setup & Backup Documentation

This directory contains the complete backup of Om's Jellyfin configuration, custom scripts, plugins, and startup behavior.

## Directory Structure
- `launcher/`
  - `launch-jellyfin.vbs` - The VBScript launcher that checks if `jellyfin.exe` is running, starts it silently in the background if not, waits for HTTP 200 on port 8096, and opens the Brave Web App (`--app="http://jellyfin.local:8096"`).
  - `Jellyfin.lnk` - Start menu shortcut pointing to `wscript.exe "%USERPROFILE%\launch-jellyfin.vbs"` with the Jellyfin icon (`C:\Program Files\Jellyfin\Server\icon.ico`).
- `plugins/configurations/`
  - `Jellyfin.Plugin.JavaScriptInjector.xml` - Injected script configuration including the "Hide Player Controls (G Key)" script.
  - `Jellyfin.Plugin.JellyfinEnhanced.xml` - Complete configuration for ratings badges, TMDB/IMDB/RottenTomatoes integrations, pause screen overlays, spoiler guards.
  - `Jellyfin.Plugin.FileTransformation.xml` - Prerequisite dependency for web transformations.
  - `Jellyfin.Plugin.QueueOsd.xml` - Player queue overlay controls.
  - `Jellyfin.Plugin.OpenSubtitles.xml` - Subtitles downloader plugin config.
  - Subfolders: `Jellyfin.Plugin.JellyfinEnhanced/`, `Jellyfin.Plugin.PluginPages/`
- `scripts/`
  - `hide-controls.js` - Standalone JavaScript / UserScript code for the 'G' key shortcut (hides OSD, top header, pause screen overlay, queue, but keeps cursor visible).
- `server-config/`
  - `system.xml` - Core server settings + custom plugin repositories list:
    1. Jellyfin Stable: `https://repo.jellyfin.org/files/plugin/manifest.json`
    2. Jellyfin Player Queue: `https://raw.githubusercontent.com/k1k4k/jellyfin-player-queue/main/manifest.json`
    3. Jellyfin Enhanced / JS Injector (v12): `https://raw.githubusercontent.com/n00bcodr/jellyfin-plugins/main/12/manifest.json`
    4. File Transformation: `https://www.iamparadox.dev/jellyfin/plugins/manifest.json`
  - `network.xml` - Network and port bindings.
  - `encoding.xml` - Transcoding configurations.

## Auto-Start Policy
- `JellyfinTray` was removed from `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run`.
- Jellyfin does NOT run on Windows startup; it starts exclusively on-demand when the user clicks the `Jellyfin` Brave shortcut.

## Future Restore Procedure
1. Copy `launcher\launch-jellyfin.vbs` to `%USERPROFILE%\launch-jellyfin.vbs`.
2. Copy `launcher\Jellyfin.lnk` to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Jellyfin.lnk`.
3. Ensure `JellyfinTray` is deleted from `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run`.
4. Add the 4 plugin repository URLs from `server-config\system.xml` into Dashboard -> Plugins -> Repositories.
5. Install: `Jellyfin Enhanced`, `JavaScript Injector`, `File Transformation`, `Jellyfin Player Queue`, `Open Subtitles`.
6. Restore XML configuration files from `plugins\configurations\` to `%ProgramData%\Jellyfin\Server\plugins\configurations\`.
7. Restart Jellyfin.
