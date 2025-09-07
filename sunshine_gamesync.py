import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

GAMES_DIR = r"Z:\xxxx\xxxx"  # <-- To the games directory
# EXE_NAME = "game.exe"  # set None if you want to detect any exe file
EXE_NAME = None

OUTPUT_FILE = "H:\\games.json"  # final JSON file (path+)


def make_entry(name, exe_path, working_dir):
    """Builds one game entry"""
    return {
        "auto-detach": True,
        "cmd": f"\"{exe_path}\"",
        "elevated": False,
        "exclude-global-prep-cmd": False,
        "exit-timeout": 5,
        "image-path": "",
        "name": name,
        "output": "",
        "wait-all": True,
        "working-dir": working_dir
    }


games = {}  # {folder_name: dict entry}


def scan_all():
    """Initial scan of games folder"""
    global games
    games.clear()
    if not os.path.exists(GAMES_DIR):
        print(f"[ERROR] {GAMES_DIR} not found!")
        return

    for folder in os.listdir(GAMES_DIR):
        folder_path = os.path.join(GAMES_DIR, folder)
        if os.path.isdir(folder_path):
            exe_path = None
            if EXE_NAME:
                candidate = os.path.join(folder_path, EXE_NAME)
                if os.path.isfile(candidate):
                    exe_path = candidate
            else:
                for f in os.listdir(folder_path):
                    if f.lower().endswith(".exe"):
                        exe_path = os.path.join(folder_path, f)
                        break

            if exe_path:
                games[folder] = make_entry(folder, exe_path, folder_path)

    print("\n[INITIAL SCAN]")
    for g, entry in games.items():
        print(f" - {g}: {entry['cmd']}")
    print("--------------\n")


class GameHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            self.check_folder(event.src_path)
        else:
            self.check_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            folder = os.path.basename(event.src_path)
            if folder in games:
                print(f"[REMOVED GAME] {folder}")
                games.pop(folder, None)
        else:
            folder = os.path.basename(os.path.dirname(event.src_path))
            if folder in games and games[folder]["cmd"].strip('"') == event.src_path:
                print(f"[EXE REMOVED] {folder}")
                games.pop(folder, None)

    def check_folder(self, folder_path):
        folder = os.path.basename(folder_path)
        if folder in games:
            return

        exe_path = None
        if EXE_NAME:
            candidate = os.path.join(folder_path, EXE_NAME)
            if os.path.isfile(candidate):
                exe_path = candidate
        else:
            for f in os.listdir(folder_path):
                if f.lower().endswith(".exe"):
                    exe_path = os.path.join(folder_path, f)
                    break

        if exe_path:
            games[folder] = make_entry(folder, exe_path, folder_path)
            print(f"[NEW GAME DETECTED] {folder} -> {exe_path}")

    def check_file(self, file_path):
        if EXE_NAME:
            if os.path.basename(file_path).lower() == EXE_NAME.lower():
                folder = os.path.basename(os.path.dirname(file_path))
                games[folder] = make_entry(folder, file_path, os.path.dirname(file_path))
                print(f"[EXE ADDED] {folder} -> {file_path}")
        elif file_path.lower().endswith(".exe"):
            folder = os.path.basename(os.path.dirname(file_path))
            if folder not in games:
                games[folder] = make_entry(folder, file_path, os.path.dirname(file_path))
                print(f"[EXE ADDED] {folder} -> {file_path}")


def save_json():
    """Save current game list as JSON file"""
    formated_json = {
        "apps": [],
        "env": {}
    }
    # put games in alphabetical order
    formated_json["apps"] = sorted(games.values(), key=lambda x: x["name"].lower())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(formated_json, f, indent=4)
    print(f"\n[JSON SAVED] -> {OUTPUT_FILE}")


if __name__ == "__main__":
    scan_all()
    save_json()  # Save after initial scan

    handler = GameHandler()
    observer = Observer()
    observer.schedule(handler, GAMES_DIR, recursive=True)
    observer.start()
    print("Watching for updates... CTRL+C to stop.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    save_json()  # Save again when stopping
