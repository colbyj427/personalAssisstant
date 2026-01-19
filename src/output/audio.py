import subprocess

import subprocess
import sys
import os

def play_chime(path="./src/output/sounds/chime.wav"):
    if not os.path.exists(path):
        print(f"[WARN] Chime file not found: {path}")
        return

    try:
        if sys.platform == "darwin":  # macOS
            subprocess.Popen(["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:  # fallback for Linux / Pi
            subprocess.Popen(["aplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[WARN] Failed to play chime: {e}")
