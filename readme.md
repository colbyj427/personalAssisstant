### Setup

- Create a python virtual environment.
    - python3 -m venv .venv
    - source .venv/bin/activate
- activate the environment.
- Run this: pip install -r requirements.txt

### LLM Model

Gemma-2b-it
https://huggingface.co/google/gemma-2b-it

pip install huggingface_hub
huggingface-cli login (enter the token generted on hugging face)
mkdir src/Agents/models
huggingface-cli download google/gemma-2-2b-it \
  --local-dir ./src/Agents/models/gemma-2-2b-it \
  --local-dir-use-symlinks False

### Transcription

Whisper
git repo:
https://github.com/ggml-org/whisper.cpp
https://github.com/ggerganov/whisper.cpp

- git clone https://github.com/ggerganov/whisper.cpp
- cd whisper.cpp
- sh ./models/download-ggml-model.sh base.en
- cmake -B build -DWHISPER_SDL2=ON
- cmake --build build -j --config Release
- (From whisper.cpp directory) ./build/bin/whisper-stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000

### Wake Word

Wake word trainings should be placed in src/input/whisper/wakeWords

### Running the Application

- From the personalAssisstant directory, run: python3 ./src/assisstant.py

