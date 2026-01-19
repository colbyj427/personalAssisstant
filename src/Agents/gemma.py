import torch
from transformers import pipeline

class GemmaAgent:
    def __init__(self, model_path="./src/Agents/models/gemma-2-2b-it"):
        """Load model once during initialization"""
        print("Loading Gemma model...")
        
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        self.pipe = pipeline(
            "text-generation",
            model=model_path,
            model_kwargs={"torch_dtype": torch.float16 if device == "mps" else torch.float32},
            device=device
        )
        
        print(f"Model loaded on {device}!")
    
    def generate(self, prompt, max_tokens=200):
        """Generate response (fast, reuses loaded model)"""
        messages = [{"role": "user", "content": prompt}]
        outputs = self.pipe(messages, max_new_tokens=max_tokens)
        return outputs[0]["generated_text"][-1]["content"]

# Usage
agent = GemmaAgent()  # Load once (10 seconds)

# Now these are fast (1-5 seconds each)
response1 = agent.generate("Hello!")
response2 = agent.generate("What's 2+2?")
response3 = agent.generate("Tell me a joke")