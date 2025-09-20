#!/usr/bin/env python3
"""
Simple wrapper to use your custom llama.cpp build with memori
This bypasses Ollama and uses your Metal-optimized llama.cpp directly
"""

import subprocess
import json
import tempfile
import os
from typing import Dict, Any, List

class LlamaCppWrapper:
    def __init__(self, model_path: str, llama_cpp_path: str = "/Users/user/llama.cpp/build/bin/llama-cli"):
        self.model_path = model_path
        self.llama_cpp_path = llama_cpp_path
        
    def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Generate text using llama.cpp with Metal AMD eGPU support"""
        
        # Create a temporary file for the prompt
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(prompt)
            prompt_file = f.name
        
        try:
            # Run llama.cpp with Metal support
            cmd = [
                self.llama_cpp_path,
                "-m", self.model_path,
                "-f", prompt_file,
                "-n", str(max_tokens),
                "--temp", str(temperature),
                "--verbose"  # This will show GPU usage
            ]
            
            print(f"🚀 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return f"Error: {result.stderr}"
            
            # Print verbose output to see GPU usage
            print("📊 Verbose Output:")
            print(result.stderr)
            print("=" * 50)
            
            # Extract the generated text (everything after the prompt)
            output = result.stdout
            if prompt in output:
                generated = output.split(prompt)[-1].strip()
            else:
                generated = output.strip()
                
            return generated
            
        finally:
            # Clean up temporary file
            if os.path.exists(prompt_file):
                os.unlink(prompt_file)
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Simple chat interface"""
        # Convert messages to a single prompt
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                prompt += f"<|user|>\n{content}\n"
            elif role == "assistant":
                prompt += f"<|assistant|>\n{content}\n"
        
        prompt += "<|assistant|>\n"
        return self.generate(prompt)

def test_llama_cpp_wrapper():
    """Test the wrapper with your TinyLlama model"""
    print("🧪 Testing LlamaCpp Wrapper with AMD eGPU")
    print("=" * 50)
    
    # Initialize wrapper with your Granite Code 34B model
    wrapper = LlamaCppWrapper("/Users/user/llama.cpp/models/granite-code-34b.gguf")
    
    # Test simple generation
    print("📝 Testing simple generation...")
    response = wrapper.generate("Hello! Can you tell me a short joke?", max_tokens=50)
    print(f"Response: {response}")
    print()
    
    # Test chat interface
    print("💬 Testing chat interface...")
    messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    response = wrapper.chat(messages)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_llama_cpp_wrapper()
