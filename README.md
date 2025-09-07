# Sunshine GameSync

`sunshine_gamesync.py` is a Python script that automatically scans your game library, generates a valid **apps.json** file, and keeps it updated for [Sunshine](https://github.com/LizardByte/Sunshine).  

This is useful if you have multiple games organized into folders (each with a `Game.exe` inside) and want them to appear automatically in the Sunshine web UI and Moonlight.

---

## 📂 Folder Structure Example

Your game directory should look like this:
---
Games/

├─ Wafer Renyah/

│ └─ Renyah.exe

├─ Doom Eternal/

│ └─ Game.exe

└─ Hollow Knight/

  └─ Game.exe

Each subfolder = one game.  
The script will map:
- **name** → folder name  
- **cmd** → full path to `.exe`  
- **working-dir** → the game folder  

---

## ⚡ Features
- Scans all subfolders for `Game.exe`.
- Generates/updates a proper `apps.json` file.
- Removes deleted games automatically.
- Runs as a lightweight watcher (near 0% CPU).
- JSON format matches Sunshine’s expected schema.

---

## 🔧 Requirements
- Python **3.9+**
- [watchdog](https://pypi.org/project/watchdog/)

Install dependencies:
```bash
pip install watchdog
```

## 📝 Configuration
By default, the script:
- Watches the Games/ folder.
- Writes apps.json to:
```shell
%LOCALAPPDATA%\GameWatcher\games.json
```
  (You can copy this into your Sunshine config folder or symlink it.)
- You can edit the script to change:
  GAMES_DIR → where your games are stored.
  OUTPUT_FILE → where the generated JSON should be saved.

## 🔄 Autostart on Windows
- Create a shortcut to sunshine_gamesync.py.
- Place it in: 
  ```shell
  shell:startup
  ```
  (Run via Win+R).
- Sunshine will always have the latest apps list at boot.



