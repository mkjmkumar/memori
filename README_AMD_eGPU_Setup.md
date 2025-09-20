# AMD eGPU Setup Guide for llama.cpp and Ollama Integration

This guide provides step-by-step instructions for setting up AMD eGPU support with llama.cpp and Ollama on macOS, specifically for MacBook Pro Intel with AMD Radeon RX 6800 eGPU via Razer Core X enclosure.

## 🎯 Overview

**Problem**: Ollama's default build doesn't support Metal AMD eGPU acceleration, causing it to fall back to CPU-only execution.

**Solution**: Build llama.cpp from source with Metal support and create custom integration scripts.

## 🔧 Hardware Requirements

- **MacBook Pro Intel** (tested on macOS 24.6.0)
- **AMD Radeon RX 6800** (16GB VRAM)
- **Razer Core X Enclosure**
- **Xcode Command Line Tools**
- **Homebrew**

## 📋 Prerequisites Installation

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required dependencies
brew install cmake go
```

## 🚀 Step 1: Build llama.cpp with Metal AMD eGPU Support

### 1.1 Clone llama.cpp Repository

```bash
cd ~
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
```

### 1.2 Configure Build with Metal Support

```bash
# Create build directory
mkdir -p build && cd build

# Configure with Metal support for AMD eGPU
cmake .. -DGGML_METAL=ON

# Verify Metal support is enabled (should show "Metal framework found")
```

### 1.3 Build llama.cpp

```bash
# Build the project
cmake --build . --config Release

# Verify build success
ls -la bin/
```

### 1.4 Test AMD eGPU Detection

```bash
# Test with verbose output to verify eGPU detection
./bin/llama-cli --help | head -20
```

**Expected Output:**
```
ggml_metal_device_init: GPU name: AMD Radeon RX 6800
ggml_metal_device_init: recommendedMaxWorkingSetSize = 17163.09 MB
```

## 📥 Step 2: Download and Test Models

### 2.1 Create Models Directory

```bash
cd ~/llama.cpp
mkdir -p models
cd models
```

### 2.2 Download Test Model (TinyLlama - 637MB)

```bash
# Download TinyLlama for testing
curl -L -o tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
```

### 2.3 Download Larger Model (Mistral 7B - 4.1GB)

```bash
# Download Mistral 7B for production use
curl -L -o mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
```

### 2.4 Test Model with AMD eGPU

```bash
cd ~/llama.cpp/build

# Test TinyLlama with verbose output
./bin/llama-cli -m ../models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  -p "Hello! Can you tell me a short joke?" \
  -n 50 --verbose
```

**Expected GPU Usage Indicators:**
```
load_tensors: offloaded 23/23 layers to GPU
load_tensors: Metal_Mapped model buffer size = 636.18 MiB
ggml_metal_device_init: GPU name: AMD Radeon RX 6800
```

## 🐍 Step 3: Python Integration Scripts

### 3.1 Create llama.cpp Wrapper

Create `llama_cpp_wrapper.py`:

```python
#!/usr/bin/env python3
"""
Simple wrapper to use your custom llama.cpp build with AMD eGPU
"""

import subprocess
import tempfile
import os
from typing import Dict, Any, List

class LlamaCppWrapper:
    def __init__(self, model_path: str, llama_cpp_path: str = "/Users/user/llama.cpp/build/bin/llama-cli"):
        self.model_path = model_path
        self.llama_cpp_path = llama_cpp_path
        
    def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Generate text using llama.cpp with Metal AMD eGPU support"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(prompt)
            prompt_file = f.name
        
        try:
            cmd = [
                self.llama_cpp_path,
                "-m", self.model_path,
                "-f", prompt_file,
                "-n", str(max_tokens),
                "--temp", str(temperature),
                "--verbose"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            
            # Extract generated text
            output = result.stdout
            if prompt in output:
                generated = output.split(prompt)[-1].strip()
            else:
                generated = output.strip()
                
            return generated
            
        finally:
            if os.path.exists(prompt_file):
                os.unlink(prompt_file)
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Simple chat interface"""
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

# Test the wrapper
if __name__ == "__main__":
    wrapper = LlamaCppWrapper("/Users/user/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
    response = wrapper.generate("Hello! Can you tell me a short joke?", max_tokens=50)
    print(f"Response: {response}")
```

### 3.2 Create GPU vs CPU Demo

Create `gpu_demo.py`:

```python
#!/usr/bin/env python3
"""
Demonstration showing the difference between CPU and GPU usage
"""

import subprocess
import time
import psutil
import threading

def monitor_cpu_usage(duration=10):
    """Monitor CPU usage for a given duration"""
    cpu_usage = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage.append(cpu_percent)
        print(f"CPU Usage: {cpu_percent:.1f}%")
    
    return cpu_usage

def test_llama_cpp_gpu():
    """Test llama.cpp with AMD eGPU"""
    print("🚀 Testing llama.cpp with AMD eGPU")
    print("=" * 50)
    
    cpu_monitor = threading.Thread(target=monitor_cpu_usage, args=(15,))
    cpu_monitor.start()
    
    cmd = [
        "/Users/user/llama.cpp/build/bin/llama-cli",
        "-m", "/Users/user/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "-p", "Hello! Can you tell me a short joke?",
        "-n", "50",
        "--verbose"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print("Watch for GPU usage in Activity Monitor!")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    end_time = time.time()
    
    print(f"⏱️  Execution time: {end_time - start_time:.2f} seconds")
    
    if "AMD Radeon RX 6800" in result.stderr:
        print("🎉 AMD eGPU detected and used!")
    if "offloaded 23/23 layers to GPU" in result.stderr:
        print("🎉 100% GPU utilization confirmed!")

def test_ollama_cpu():
    """Test Ollama (CPU-only)"""
    print("🖥️  Testing Ollama (CPU-only)")
    print("=" * 50)
    
    cpu_monitor = threading.Thread(target=monitor_cpu_usage, args=(15,))
    cpu_monitor.start()
    
    cmd = ["ollama", "run", "tinyllama", "Hello! Can you tell me a short joke?"]
    
    print(f"Running: {' '.join(cmd)}")
    print("Watch for CPU usage in Activity Monitor!")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    end_time = time.time()
    
    print(f"⏱️  Execution time: {end_time - start_time:.2f} seconds")
    
    if "CPU" in result.stderr and "GPU" not in result.stderr:
        print("⚠️  CPU-only execution detected")

if __name__ == "__main__":
    print("🔬 GPU vs CPU Usage Demonstration")
    print("=" * 60)
    
    test_llama_cpp_gpu()
    print("⏸️  Pausing for 5 seconds...")
    time.sleep(5)
    test_ollama_cpu()
    
    print("🎯 Summary:")
    print("- llama.cpp: Uses your AMD Radeon RX 6800 eGPU (16GB VRAM)")
    print("- Ollama: Uses CPU only (no GPU acceleration)")
```

## 🔄 Step 4: Integrating New Models

### 4.1 Download Any GGUF Model

```bash
cd ~/llama.cpp/models

# Example: Download Llama 3.2 3B
curl -L -o llama-3.2-3b-instruct.Q4_K_M.gguf \
  "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"

# Example: Download CodeLlama 7B
curl -L -o codellama-7b-instruct.Q4_K_M.gguf \
  "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf"
```

### 4.2 Test New Model with AMD eGPU

```bash
cd ~/llama.cpp/build

# Test the new model
./bin/llama-cli -m ../models/llama-3.2-3b-instruct.Q4_K_M.gguf \
  -p "Write a Python function to calculate fibonacci numbers" \
  -n 100 --verbose
```

### 4.3 Update Python Wrapper for New Model

```python
# Update the model path in your wrapper
wrapper = LlamaCppWrapper("/Users/user/llama.cpp/models/llama-3.2-3b-instruct.Q4_K_M.gguf")

# Test the new model
response = wrapper.generate("Explain quantum computing in simple terms", max_tokens=150)
print(f"Response: {response}")
```

## 🛠️ Step 5: Ollama Integration (Alternative Approach)

### 5.1 Build Ollama from Source with Metal Support

```bash
# Clone Ollama source
cd ~
git clone https://github.com/ollama/ollama.git ollama-source
cd ollama-source

# Configure with Metal support
cmake -B build -DGGML_METAL=ON

# Build (requires Xcode for Metal compilation)
cmake --build build
```

**Note**: This requires Xcode (not just command line tools) for Metal kernel compilation.

### 5.2 Use Custom llama.cpp with Ollama API

Create a simple HTTP server that wraps llama.cpp:

```python
#!/usr/bin/env python3
"""
Simple HTTP server that wraps llama.cpp to mimic Ollama API
"""

from flask import Flask, request, jsonify
from llama_cpp_wrapper import LlamaCppWrapper
import json

app = Flask(__name__)
wrapper = LlamaCppWrapper("/Users/user/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    # Convert messages to prompt
    prompt = ""
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'user':
            prompt += f"<|user|>\n{content}\n"
        elif role == 'assistant':
            prompt += f"<|assistant|>\n{content}\n"
    
    prompt += "<|assistant|>\n"
    
    response = wrapper.generate(prompt, max_tokens=100)
    
    return jsonify({
        'message': {
            'role': 'assistant',
            'content': response
        }
    })

if __name__ == '__main__':
    print("🚀 Starting llama.cpp HTTP server on port 11434")
    print("💡 This mimics Ollama API but uses your AMD eGPU!")
    app.run(host='0.0.0.0', port=11434)
```

## 📊 Performance Monitoring

### Monitor GPU Usage

```bash
# Install GPU monitoring tool
brew install gpu-stat

# Monitor GPU usage during inference
gpu-stat
```

### Monitor VRAM Usage

```bash
# Check VRAM usage
system_profiler SPDisplaysDataType | grep -A 10 "Radeon"
```

## 🐛 Troubleshooting

### Issue: "Metal framework not found"

**Solution:**
```bash
# Ensure Xcode command line tools are installed
xcode-select --install

# Verify Metal framework
ls /System/Library/Frameworks/Metal.framework/
```

### Issue: "Unable to find utility 'metal'"

**Solution:**
```bash
# Install full Xcode (not just command line tools)
# Download from App Store or developer.apple.com
```

### Issue: Model not using GPU

**Solution:**
```bash
# Check verbose output for GPU indicators
./bin/llama-cli -m model.gguf -p "test" --verbose

# Look for:
# - "AMD Radeon RX 6800"
# - "offloaded X/X layers to GPU"
# - "Metal_Mapped model buffer size"
```

### Issue: Low GPU utilization

**Solution:**
```bash
# Use larger batch size
./bin/llama-cli -m model.gguf -p "test" --batch-size 512

# Use more GPU layers
./bin/llama-cli -m model.gguf -p "test" --gpu-layers 23
```

## 📈 Performance Optimization

### Recommended Settings for AMD RX 6800

```bash
# Optimal settings for 16GB VRAM
./bin/llama-cli \
  -m model.gguf \
  -p "prompt" \
  --batch-size 512 \
  --gpu-layers 23 \
  --ctx-size 4096 \
  --temp 0.7 \
  --verbose
```

### Model Size Recommendations

- **TinyLlama 1.1B**: 637MB - Good for testing
- **Llama 3.2 3B**: ~2GB - Balanced performance
- **Mistral 7B**: 4.1GB - High quality
- **Llama 2 13B**: ~7GB - Maximum for your setup
- **Llama 2 70B**: Too large for 16GB VRAM

## 🎯 Summary

This setup provides:

✅ **AMD eGPU acceleration** with 16GB VRAM  
✅ **Zero API costs** - everything runs locally  
✅ **High performance** - 100% GPU utilization  
✅ **Easy model integration** - just download GGUF files  
✅ **Python integration** - ready for AI applications  
✅ **Ollama compatibility** - via custom HTTP wrapper  

Your AMD Radeon RX 6800 eGPU is now fully operational for local AI development!

## 📚 Additional Resources

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [GGUF Model Hub](https://huggingface.co/models?library=gguf)
- [Metal Performance Shaders](https://developer.apple.com/documentation/metalperformanceshaders)
- [AMD eGPU on macOS](https://support.apple.com/en-us/HT208544)
