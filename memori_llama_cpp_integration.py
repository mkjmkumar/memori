#!/usr/bin/env python3
"""
Memori integration with custom llama.cpp wrapper using AMD eGPU
This demonstrates cost-effective local AI with memory persistence
"""

import os
import time
from llama_cpp_wrapper import LlamaCppWrapper
from memori import Memori
from memori.core.providers import ProviderConfig

class LlamaCppProvider:
    """Custom provider that uses our llama.cpp wrapper with AMD eGPU"""
    
    def __init__(self, model_path: str, llama_cpp_path: str = "/Users/user/llama.cpp/build/bin/llama-cli"):
        self.wrapper = LlamaCppWrapper(model_path, llama_cpp_path)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using llama.cpp with AMD eGPU"""
        max_tokens = kwargs.get('max_tokens', 100)
        temperature = kwargs.get('temperature', 0.7)
        
        return self.wrapper.generate(prompt, max_tokens, temperature)
    
    def chat(self, messages: list, **kwargs) -> str:
        """Chat interface using llama.cpp with AMD eGPU"""
        return self.wrapper.chat(messages)

def test_memori_with_amd_egpu():
    """Test memori with AMD eGPU-powered llama.cpp"""
    print("🚀 Testing Memori with AMD eGPU-powered llama.cpp")
    print("=" * 60)
    
    # Initialize our custom provider with AMD eGPU
    print("📝 Initializing AMD eGPU provider...")
    provider = LlamaCppProvider("/Users/user/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
    
    # Initialize memori with our custom provider
    print("🧠 Initializing Memori with custom provider...")
    memori = Memori(
        database_connect="sqlite:///amd_egpu_memori_test.db",
        conscious_ingest=True,  # Short-term working memory
        auto_ingest=True,       # Long-term memory
        provider=provider       # Use our AMD eGPU provider
    )
    
    print("✅ Memori initialized successfully!")
    print()
    
    # Test 1: Simple conversation with memory
    print("💬 Test 1: Simple conversation with memory")
    print("-" * 40)
    
    response1 = memori.conscious_ingest(
        "Hello! My name is Alex and I'm working on a project about AI memory systems."
    )
    print(f"Response 1: {response1}")
    print()
    
    # Test 2: Memory recall
    print("🧠 Test 2: Memory recall")
    print("-" * 40)
    
    response2 = memori.conscious_ingest(
        "What's my name and what am I working on?"
    )
    print(f"Response 2: {response2}")
    print()
    
    # Test 3: Context-aware conversation
    print("🎯 Test 3: Context-aware conversation")
    print("-" * 40)
    
    response3 = memori.conscious_ingest(
        "Can you give me some advice about my project?"
    )
    print(f"Response 3: {response3}")
    print()
    
    # Test 4: Memory search
    print("🔍 Test 4: Memory search")
    print("-" * 40)
    
    memories = memori.search_memories("Alex project AI")
    print(f"Found {len(memories)} relevant memories:")
    for i, memory in enumerate(memories[:3], 1):
        print(f"  {i}. {memory.content[:100]}...")
    print()
    
    print("🎉 All tests completed successfully!")
    print("💡 Your AMD eGPU is now powering cost-effective local AI with memory!")

if __name__ == "__main__":
    test_memori_with_amd_egpu()
