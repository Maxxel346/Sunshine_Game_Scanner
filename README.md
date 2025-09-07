# Sunshine GameSync

`sunshine_gamesync.py` is a Python script that automatically scans your game library, generates a valid **apps.json** file, and keeps it updated for [Sunshine](https://github.com/LizardByte/Sunshine).  

This is useful if you have multiple games organized into folders (each with a `Game.exe` inside) and want them to appear automatically in the Sunshine web UI and Moonlight.

---

## 📂 Folder Structure Example

Your game directory should look like this:

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
