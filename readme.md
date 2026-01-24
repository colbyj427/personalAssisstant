### Setup

- Create a python virtual environment.
    - python3 -m venv .venv
    - source .venv/bin/activate
- activate the environment.
- Run this: pip install -r requirements.txt

### LLM Model

Gemma-2b-it
https://huggingface.co/google/gemma-2b-it

### Transcription

Whisper
git repo:
https://github.com/ggml-org/whisper.cpp

- git clone https://github.com/ggerganov/whisper.cpp
- cd whisper.cpp
- sh ./models/download-ggml-model.sh base.en
- cmake -B build -DWHISPER_SDL2=ON
- cmake --build build -j --config Release
- (From whisper.cpp directory) ./build/bin/whisper-stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000

### Wake Word

Wake word trainings should be placed in src/input/whisper/wakeWords
