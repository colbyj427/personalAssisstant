import wave
import math
import struct

def generate_chime(filename="sounds/chime.wav", duration=0.2, freq=880, volume=0.5, sample_rate=44100):
    """
    Generate a simple sine-wave chime and save it as a WAV file.
    """
    n_samples = int(sample_rate * duration)
    wav_file = wave.open(filename, "w")
    wav_file.setparams((1, 2, sample_rate, n_samples, "NONE", "not compressed"))

    for i in range(n_samples):
        sample = volume * math.sin(2 * math.pi * freq * i / sample_rate)
        wav_file.writeframes(struct.pack('<h', int(sample * 32767.0)))

    wav_file.close()
    print(f"[INFO] Generated chime WAV: {filename}")

# Example usage
generate_chime()
