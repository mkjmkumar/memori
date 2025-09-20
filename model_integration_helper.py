#!/usr/bin/env python3
"""
Model Integration Helper for AMD eGPU Setup
This script helps you easily integrate new GGUF models with your AMD eGPU setup
"""

import os
import subprocess
import requests
from pathlib import Path
import argparse

class ModelIntegrationHelper:
    def __init__(self, llama_cpp_path="/Users/user/llama.cpp/build/bin/llama-cli", 
                 models_dir="/Users/user/llama.cpp/models"):
        self.llama_cpp_path = llama_cpp_path
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
    def download_model(self, model_url: str, filename: str = None):
        """Download a GGUF model from URL"""
        if not filename:
            filename = model_url.split("/")[-1]
        
        model_path = self.models_dir / filename
        
        print(f"📥 Downloading {filename}...")
        print(f"URL: {model_url}")
        print(f"Destination: {model_path}")
        
        try:
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end="", flush=True)
            
            print(f"\n✅ Download complete: {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None
    
    def test_model_gpu(self, model_path: str, test_prompt: str = "Hello! Can you tell me a short joke?"):
        """Test if a model uses AMD eGPU properly"""
        print(f"🧪 Testing model: {model_path}")
        print(f"Prompt: {test_prompt}")
        print("=" * 60)
        
        cmd = [
            self.llama_cpp_path,
            "-m", str(model_path),
            "-p", test_prompt,
            "-n", "50",
            "--verbose"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Model test failed: {result.stderr}")
                return False
            
            # Check for GPU usage indicators
            gpu_indicators = [
                "AMD Radeon RX 6800",
                "offloaded",
                "layers to GPU",
                "Metal_Mapped model buffer size"
            ]
            
            gpu_detected = any(indicator in result.stderr for indicator in gpu_indicators)
            
            if gpu_detected:
                print("🎉 AMD eGPU detected and working!")
                print("📊 GPU Usage Indicators:")
                for line in result.stderr.split('\n'):
                    if any(indicator in line for indicator in gpu_indicators):
                        print(f"   {line}")
            else:
                print("⚠️  No GPU usage detected - model may be using CPU only")
            
            # Extract and display response
            if result.stdout:
                response = result.stdout.strip()
                print(f"\n💬 Model Response:")
                print(f"   {response[:200]}{'...' if len(response) > 200 else ''}")
            
            return gpu_detected
            
        except subprocess.TimeoutExpired:
            print("⏰ Model test timed out")
            return False
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def create_wrapper_script(self, model_path: str, model_name: str):
        """Create a Python wrapper script for the model"""
        wrapper_content = f'''#!/usr/bin/env python3
"""
Wrapper for {model_name} with AMD eGPU support
"""

from llama_cpp_wrapper import LlamaCppWrapper

# Initialize wrapper with your model
wrapper = LlamaCppWrapper("{model_path}")

def chat(prompt: str, max_tokens: int = 100):
    """Chat with the model"""
    return wrapper.generate(prompt, max_tokens)

if __name__ == "__main__":
    # Test the model
    response = chat("Hello! How are you?")
    print(f"Response: {{response}}")
'''
        
        script_path = self.models_dir / f"{model_name}_wrapper.py"
        with open(script_path, 'w') as f:
            f.write(wrapper_content)
        
        print(f"📝 Created wrapper script: {script_path}")
        return script_path
    
    def list_available_models(self):
        """List all available GGUF models in the models directory"""
        print("📋 Available Models:")
        print("=" * 40)
        
        gguf_files = list(self.models_dir.glob("*.gguf"))
        
        if not gguf_files:
            print("No GGUF models found in models directory")
            return []
        
        for i, model_file in enumerate(gguf_files, 1):
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"{i}. {model_file.name} ({size_mb:.1f} MB)")
        
        return gguf_files
    
    def get_model_info(self, model_path: str):
        """Get information about a model"""
        print(f"📊 Model Information: {model_path}")
        print("=" * 50)
        
        cmd = [self.llama_cpp_path, "-m", str(model_path), "--help"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Try to get model info by running with a simple prompt
            info_cmd = [
                self.llama_cpp_path,
                "-m", str(model_path),
                "-p", "test",
                "-n", "1",
                "--verbose"
            ]
            
            info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)
            
            # Extract model information from verbose output
            info_lines = info_result.stderr.split('\n')
            for line in info_lines:
                if any(keyword in line.lower() for keyword in ['model', 'params', 'size', 'type', 'arch']):
                    print(f"   {line}")
            
        except Exception as e:
            print(f"❌ Could not get model info: {e}")

def main():
    parser = argparse.ArgumentParser(description="Model Integration Helper for AMD eGPU")
    parser.add_argument("--download", help="Download a model from URL")
    parser.add_argument("--test", help="Test a model for GPU usage")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--info", help="Get information about a model")
    parser.add_argument("--create-wrapper", help="Create wrapper script for a model")
    parser.add_argument("--model-name", help="Name for the model (used with --create-wrapper)")
    
    args = parser.parse_args()
    
    helper = ModelIntegrationHelper()
    
    if args.download:
        model_path = helper.download_model(args.download)
        if model_path:
            print(f"✅ Model downloaded successfully: {model_path}")
            print("💡 Run with --test to verify GPU usage")
    
    elif args.test:
        model_path = Path(args.test)
        if not model_path.is_absolute():
            model_path = helper.models_dir / args.test
        
        if model_path.exists():
            helper.test_model_gpu(str(model_path))
        else:
            print(f"❌ Model not found: {model_path}")
    
    elif args.list:
        helper.list_available_models()
    
    elif args.info:
        model_path = Path(args.info)
        if not model_path.is_absolute():
            model_path = helper.models_dir / args.info
        
        if model_path.exists():
            helper.get_model_info(str(model_path))
        else:
            print(f"❌ Model not found: {model_path}")
    
    elif args.create_wrapper:
        model_path = Path(args.create_wrapper)
        if not model_path.is_absolute():
            model_path = helper.models_dir / args.create_wrapper
        
        if model_path.exists():
            model_name = args.model_name or model_path.stem
            helper.create_wrapper_script(str(model_path), model_name)
        else:
            print(f"❌ Model not found: {model_path}")
    
    else:
        print("🔧 Model Integration Helper for AMD eGPU")
        print("=" * 50)
        print("Usage examples:")
        print("  python model_integration_helper.py --list")
        print("  python model_integration_helper.py --download 'https://example.com/model.gguf'")
        print("  python model_integration_helper.py --test tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
        print("  python model_integration_helper.py --info tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
        print("  python model_integration_helper.py --create-wrapper tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --model-name tinyllama")

if __name__ == "__main__":
    main()
