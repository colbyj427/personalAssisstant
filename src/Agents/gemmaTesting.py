# import torch
# from transformers import pipeline

# pipe = pipeline(
#     "text-generation",
#     model="google/gemma-2-2b-it",
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device="mps",  # replace with "mps" to run on a Mac device
# )

# messages = [
#     {"role": "user", "content": "Who are you? Please, answer in pirate-speak."},
# ]

# outputs = pipe(messages, max_new_tokens=256)
# assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
# print(assistant_response)




# Ahoy, matey! I be Gemma, a digital scallywag, a language-slingin' parrot of the digital seas. I be here to help ye with yer wordy woes, answer yer questions, and spin ye yarns of the digital world.  So, what be yer pleasure, eh? 🦜

# from transformers import AutoTokenizer, AutoModelForCausalLM

# # Download and save to your project directory
# model_path = "src/Agents/models/gemma-2-2b-it"  # Local path in your project

# tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
# model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it")

# # Save locally
# tokenizer.save_pretrained(model_path)
# model.save_pretrained(model_path)

# print(f"Model saved to {model_path}")



# gemma_simple.py
import torch
from transformers import pipeline

# Auto-detect device
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load from local path
pipe = pipeline(
    "text-generation",
    model="./src/Agents/models/gemma-2-2b-it",
    model_kwargs={"torch_dtype": torch.float16 if device == "mps" else torch.float32},
    device=device
)

# Prompt
messages = [
    {"role": "user", "content": "What is machine learning?"}
]

# Generate
print("Generating response...\n")
outputs = pipe(messages, max_new_tokens=200)
response = outputs[0]["generated_text"][-1]["content"]

print(response)