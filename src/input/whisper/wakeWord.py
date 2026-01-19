import pvporcupine
import sounddevice as sd
import struct

RUNNING = True

# wake_word="./src/input/whisper/wakeWords/Shakira_en_mac_v4_0_0/Shakira_en_mac_v4_0_0.ppn"
# wake_word="./src/input/whisper/wakeWords/Shakira_en_raspberry-pi_v4_0_0/Shaqira_en_raspberry-pi_v4_0_0.ppn"
# wake_word="porcupine"  # built-in keyword
def listen_for_wake_word(wake_word="porcupine", access_key="+KUkPFsG1naLMZ+N9fJICz4kNJbb0pjP7iKMJQNvg4NmpsMcENuRQQ=="):
    global RUNNING
    RUNNING = True
    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=[wake_word]
        # keyword_paths=[wake_word]
    )

    def audio_callback(indata, frames, time, status):
        pcm = struct.unpack_from("h" * frames, indata)
        result = porcupine.process(pcm)
        if result >= 0:
            global RUNNING
            RUNNING = False
            # raise KeyboardInterrupt  # wake word detected

    try:
        with sd.InputStream(
            channels=1,
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            dtype='int16',
            callback=audio_callback
        ):
            print("Listening for wake word...")
            while RUNNING:
                pass
    except Exception:
        print("ERROR listening for wake word")
        raise Exception
    finally:
        print("Wake word detected!")
        porcupine.delete()
    
    return True

if __name__ == "__main__":
    listen_for_wake_word()