import subprocess
import time
import signal
import sys
from Agents.gemma import GemmaAgent
from input.whisper.wakeWord import listen_for_wake_word
from input.whisper.micMonitoring import WhisperStreamer
from output.audio import play_chime

# ======================
# CONFIG
# ======================

WHISPER_CMD = [
    "./build/bin/whisper-stream",
    "-m", "./models/ggml-base.en.bin",
    "-t", "8",
    "--step", "500",
    "--length", "5000"
]

WAKE_COOLDOWN = 1.5      # seconds after wake word
WHISPER_COOLDOWN = 1.0   # seconds after whisper exits

# ======================
# GLOBAL STATE
# ======================

RUNNING = True


# ======================
# SIGNAL HANDLING
# ======================

def shutdown_handler(sig, frame):
    global RUNNING
    print("\n[INFO] Shutdown requested...")
    RUNNING = False

# signal.signal(signal.SIGINT, shutdown_handler)
# signal.signal(signal.SIGTERM, shutdown_handler)


# ======================
# WHISPER RUNNER
# ======================

whisper = WhisperStreamer()

# def run_whisper():
#     print("[INFO] Starting Whisper...")
#     process = subprocess.Popen(
#         WHISPER_CMD,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True
#     )

#     try:
#         for line in process.stdout:
#             if not RUNNING:
#                 break

#             line = line.strip()
#             if line:
#                 print(f"[WHISPER] {line}")

#     finally:
#         print("[INFO] Stopping Whisper...")
#         process.terminate()
#         process.wait()

def runWhisper():
    whisper.start()
    start_time = time.time()
    timeout_seconds = 5  # stop after 10 seconds of streaming

    while time.time() - start_time < timeout_seconds:
        text = whisper.get_transcription(timeout=1)
        if text:
            print("Transcribed:", text)
            # Stop early if user says "stop"
            if "stop" in text.lower():
                break

    whisper.stop()


# ======================
# WAKE WORD LOOP (mocked)
# ======================

# def listen_for_wake_word():
#     """
#     Replace this with your Porcupine loop.
#     This function should BLOCK until wake word is detected.
#     """
#     print("[INFO] Listening for wake word...")
#     time.sleep(3)  # simulate listening
#     print("[INFO] Wake word detected!")


# ======================
# MAIN LOOP
# ======================

def main():
    global RUNNING

    print("[INFO] Assistant started")

    try:
        # 0. Initialize LLM
        gemma = GemmaAgent()
        
        while RUNNING:

            # 1. Wait for wake word
            listen_for_wake_word()
            
            # 3. Run whisper (blocking)
            play_chime()

            #4. Run whisper
            runWhisper()
            text = "PLACEHOLDER"

            # 4. Whisper cooldown
            time.sleep(WHISPER_COOLDOWN)

            # 5. Send to LLM
            response = gemma.generate("User said: just tell a joke" + text)

            # 6. Respond via TTS
            print("TTS Response:", response)
            play_chime()

    finally:
        print("[INFO] Cleaning up resources...")


if __name__ == "__main__":
    main()