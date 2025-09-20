#!/usr/bin/env python3
"""
Simple script to download and integrate any model with your AMD eGPU setup
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path

def download_via_ollama(model_name: str):
    """Download model via Ollama and copy to llama.cpp models directory"""
    print(f"🔄 Downloading {model_name} via Ollama...")
    
    # Download the model
    result = subprocess.run(["ollama", "pull", model_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to download {model_name}: {result.stderr}")
        return False
    
    print(f"✅ Downloaded {model_name}")
    
    # Get the model file path
    result = subprocess.run(["ollama", "show", model_name, "--modelfile"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to get model info: {result.stderr}")
        return False
    
    # Extract the file path from the modelfile output
    lines = result.stdout.split('\n')
    model_file_path = None
    for line in lines:
        if line.startswith('FROM '):
            model_file_path = line.replace('FROM ', '').strip()
            break
    
    if not model_file_path or not os.path.exists(model_file_path):
        print(f"❌ Could not find model file for {model_name}")
        return False
    
    # Copy to llama.cpp models directory
    models_dir = "/Users/user/llama.cpp/models"
    model_filename = f"{model_name.replace(':', '-')}.gguf"
    destination = os.path.join(models_dir, model_filename)
    
    print(f"📁 Copying {model_file_path} to {destination}")
    shutil.copy2(model_file_path, destination)
    
    print(f"✅ Model integrated: {destination}")
    return destination

def download_via_huggingface(url: str, filename: str = None):
    """Download model directly from Hugging Face"""
    if not filename:
        filename = url.split('/')[-1]
    
    models_dir = "/Users/user/llama.cpp/models"
    destination = os.path.join(models_dir, filename)
    
    print(f"🔄 Downloading {url} to {destination}")
    
    # Use curl to download
    cmd = ["curl", "-L", "-o", destination, url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to download: {result.stderr}")
        return False
    
    print(f"✅ Model downloaded: {destination}")
    return destination

def test_model(model_path: str):
    """Test the model with your AMD eGPU"""
    print(f"🧪 Testing {model_path} with AMD eGPU...")
    
    cmd = [
        "/Users/user/llama.cpp/build/bin/llama-cli",
        "-m", model_path,
        "-p", "Hello! This is a test.",
        "-n", "20",
        "--verbose"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        print("✅ Model test successful!")
        print("📊 GPU Usage (look for 'offloaded X/X layers to GPU'):")
        print(result.stderr)
        return True
    else:
        print(f"❌ Model test failed: {result.stderr}")
        return False

def main():
    print("🚀 Model Download and Integration Tool")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python download_and_integrate_model.py ollama <model-name>")
        print("  python download_and_integrate_model.py huggingface <url> [filename]")
        print()
        print("Examples:")
        print("  python download_and_integrate_model.py ollama llama3.2:3b")
        print("  python download_and_integrate_model.py ollama codellama:7b")
        print("  python download_and_integrate_model.py ollama mistral:7b")
        print("  python download_and_integrate_model.py huggingface https://huggingface.co/.../model.gguf")
        return
    
    method = sys.argv[1].lower()
    
    if method == "ollama":
        if len(sys.argv) < 3:
            print("❌ Please provide a model name")
            return
        
        model_name = sys.argv[2]
        model_path = download_via_ollama(model_name)
        
        if model_path:
            test_model(model_path)
    
    elif method == "huggingface":
        if len(sys.argv) < 3:
            print("❌ Please provide a URL")
            return
        
        url = sys.argv[2]
        filename = sys.argv[3] if len(sys.argv) > 3 else None
        model_path = download_via_huggingface(url, filename)
        
        if model_path:
            test_model(model_path)
    
    else:
        print("❌ Unknown method. Use 'ollama' or 'huggingface'")

if __name__ == "__main__":
    main()
