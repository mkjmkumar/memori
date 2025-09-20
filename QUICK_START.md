# Quick Start Guide - AMD eGPU Setup

## 🚀 One-Command Setup

```bash
# Run the automated setup script
./setup_amd_egpu.sh
```

This script will:
- ✅ Install all dependencies (Homebrew, CMake, Go)
- ✅ Build llama.cpp with Metal AMD eGPU support
- ✅ Download and test TinyLlama model
- ✅ Install Python dependencies
- ✅ Configure your environment

## 🧪 Quick Test

After setup, test your AMD eGPU:

```bash
# Test GPU detection
llama-cli -m ~/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "Hello!" -n 20 --verbose
```

Look for:
- `ggml_metal_device_init: GPU name: AMD Radeon RX 6800`
- `load_tensors: offloaded 23/23 layers to GPU`

## 📥 Download New Models

```bash
# Use the helper script
python model_integration_helper.py --download "https://huggingface.co/TheBloke/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"

# Test the new model
python model_integration_helper.py --test Llama-3.2-3B-Instruct-Q4_K_M.gguf
```

## 🐍 Python Integration

```python
from llama_cpp_wrapper import LlamaCppWrapper

# Initialize with your model
wrapper = LlamaCppWrapper("~/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

# Generate text with AMD eGPU
response = wrapper.generate("Hello! How are you?", max_tokens=50)
print(response)
```

## 🔍 Troubleshooting

### GPU Not Detected
```bash
# Check GPU detection
system_profiler SPDisplaysDataType | grep -A 5 "Radeon"

# Rebuild with Metal support
cd ~/llama.cpp/build
cmake .. -DGGML_METAL=ON
cmake --build . --config Release
```

### Model Not Using GPU
```bash
# Check verbose output
llama-cli -m model.gguf -p "test" --verbose

# Look for GPU indicators in stderr output
```

## 📊 Performance Monitoring

```bash
# Monitor GPU usage
gpu-stat

# Monitor VRAM
system_profiler SPDisplaysDataType | grep -A 10 "Radeon"
```

## 🎯 Recommended Models for 16GB VRAM

- **TinyLlama 1.1B**: 637MB - Testing
- **Llama 3.2 3B**: ~2GB - Balanced
- **Mistral 7B**: 4.1GB - High quality
- **Llama 2 13B**: ~7GB - Maximum

## 📚 Full Documentation

See `README_AMD_eGPU_Setup.md` for complete setup instructions and troubleshooting.
