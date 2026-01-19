import subprocess
import threading
import time
import queue
# from src.input.whisper.wakeWord import listen_for_wake_word

class WhisperStreamer:
    def __init__(self, model_path="./src/input/whisper/whisper.cpp/models/ggml-base.en.bin", threads=8, step=500, length=5000):
        self.model_path = model_path
        self.threads = 1
        self.step = step
        self.length = length
        self.process = None
        self.queue = queue.Queue()
        self.running = False

    def _reader_thread(self, stdout):
        """Read lines from whisper-stream and put them into a queue."""
        for line in iter(stdout.readline, ''):
            line = line.strip()
            if line:
                self.queue.put(line)
        stdout.close()

    def start(self):
        """Start the whisper-stream process."""
        if self.running:
            print("Whisper is already running.")
            return

        cmd = [
            "./src/input/whisper/whisper.cpp/build/bin/whisper-stream",
            "-m", self.model_path,
            "-t", str(self.threads),
            "--step", str(self.step),
            "--length", str(self.length)
        ]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        self.running = True
        threading.Thread(target=self._reader_thread, args=(self.process.stdout,), daemon=True).start()
        print("Whisper streaming started.")

    def stop(self):
        """Stop the whisper-stream process."""
        if self.process and self.running:
            self.process.terminate()
            self.process.wait()
            self.running = False
            print("Whisper streaming stopped.")

    def get_transcription(self, timeout=None):
        """
        Get the latest transcription line from the queue.
        If timeout is specified, wait up to that many seconds.
        """
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None


# =======================
# Example usage with wake word
# =======================

def dummy_wake_word_detector():
    """Simulate a wake word detection."""
    time.sleep(2)  # wait 2 seconds
    return True

def main():
    streamer = WhisperStreamer()

    while True:
        print("Listening for wake word...")
        if dummy_wake_word_detector():
            streamer.start()
            start_time = time.time()
            timeout_seconds = 20  # stop after 10 seconds of streaming

            while time.time() - start_time < timeout_seconds:
                text = streamer.get_transcription(timeout=1)
                if text:
                    print("Transcribed:", text)
                    # Stop early if user says "stop"
                    if "stop" in text.lower():
                        break

            streamer.stop()

if __name__ == "__main__":
    main()
