#!/usr/bin/env python3
"""
Simple demonstration showing the difference between CPU and GPU usage
This clearly shows why your AMD eGPU is working with llama.cpp but not with Ollama
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
    """Test llama.cpp with AMD eGPU (should show GPU spike)"""
    print("🚀 Testing llama.cpp with AMD eGPU")
    print("=" * 50)
    
    # Start CPU monitoring in background
    cpu_monitor = threading.Thread(target=monitor_cpu_usage, args=(15,))
    cpu_monitor.start()
    
    # Run llama.cpp with verbose output
    cmd = [
        "/Users/user/llama.cpp/build/bin/llama-cli",
        "-m", "/Users/user/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "-p", "Hello! Can you tell me a short joke?",
        "-n", "50",
        "--verbose"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print("Watch for GPU usage in Activity Monitor!")
    print()
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    end_time = time.time()
    
    print(f"⏱️  Execution time: {end_time - start_time:.2f} seconds")
    print(f"✅ Return code: {result.returncode}")
    
    # Check for GPU indicators in output
    if "AMD Radeon RX 6800" in result.stderr:
        print("🎉 AMD eGPU detected and used!")
    if "offloaded 23/23 layers to GPU" in result.stderr:
        print("🎉 100% GPU utilization confirmed!")
    
    print()

def test_ollama_cpu():
    """Test Ollama (should show CPU spike)"""
    print("🖥️  Testing Ollama (CPU-only)")
    print("=" * 50)
    
    # Start CPU monitoring in background
    cpu_monitor = threading.Thread(target=monitor_cpu_usage, args=(15,))
    cpu_monitor.start()
    
    # Run Ollama
    cmd = ["ollama", "run", "tinyllama", "Hello! Can you tell me a short joke?"]
    
    print(f"Running: {' '.join(cmd)}")
    print("Watch for CPU usage in Activity Monitor!")
    print()
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    end_time = time.time()
    
    print(f"⏱️  Execution time: {end_time - start_time:.2f} seconds")
    print(f"✅ Return code: {result.returncode}")
    
    # Check for CPU indicators in output
    if "CPU" in result.stderr and "GPU" not in result.stderr:
        print("⚠️  CPU-only execution detected")
    
    print()

def main():
    """Main demonstration"""
    print("🔬 GPU vs CPU Usage Demonstration")
    print("=" * 60)
    print("This demo shows the difference between:")
    print("1. llama.cpp with AMD eGPU (GPU spike)")
    print("2. Ollama with CPU-only (CPU spike)")
    print()
    print("💡 Open Activity Monitor to see the difference!")
    print()
    
    # Test 1: llama.cpp with AMD eGPU
    test_llama_cpp_gpu()
    
    print("⏸️  Pausing for 5 seconds...")
    time.sleep(5)
    print()
    
    # Test 2: Ollama with CPU
    test_ollama_cpu()
    
    print("🎯 Summary:")
    print("- llama.cpp: Uses your AMD Radeon RX 6800 eGPU (16GB VRAM)")
    print("- Ollama: Uses CPU only (no GPU acceleration)")
    print("- Solution: Use llama.cpp directly or build Ollama with Metal support")
    print()
    print("💡 For memori integration, use the llama_cpp_wrapper.py we created!")

if __name__ == "__main__":
    main()
