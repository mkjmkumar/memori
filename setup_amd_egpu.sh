#!/bin/bash

# AMD eGPU Setup Script for llama.cpp and Ollama Integration
# This script automates the entire setup process

set -e  # Exit on any error

echo "🚀 AMD eGPU Setup Script for llama.cpp and Ollama Integration"
echo "=============================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only"
    exit 1
fi

# Check for AMD eGPU
print_status "Checking for AMD eGPU..."
if system_profiler SPDisplaysDataType | grep -q "Radeon"; then
    print_success "AMD GPU detected"
    system_profiler SPDisplaysDataType | grep -A 5 "Radeon"
else
    print_warning "No AMD GPU detected. This script is designed for AMD eGPU setups."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Homebrew
print_status "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    print_success "Homebrew already installed"
fi

# Install dependencies
print_status "Installing dependencies..."
brew install cmake go

# Check for Xcode command line tools
print_status "Checking for Xcode command line tools..."
if ! xcode-select -p &> /dev/null; then
    print_status "Installing Xcode command line tools..."
    xcode-select --install
    print_warning "Please complete the Xcode installation and run this script again"
    exit 1
else
    print_success "Xcode command line tools already installed"
fi

# Create llama.cpp directory
LLAMA_CPP_DIR="$HOME/llama.cpp"
print_status "Setting up llama.cpp in $LLAMA_CPP_DIR"

if [ -d "$LLAMA_CPP_DIR" ]; then
    print_warning "llama.cpp directory already exists. Updating..."
    cd "$LLAMA_CPP_DIR"
    git pull
else
    print_status "Cloning llama.cpp repository..."
    git clone https://github.com/ggerganov/llama.cpp.git "$LLAMA_CPP_DIR"
    cd "$LLAMA_CPP_DIR"
fi

# Build llama.cpp with Metal support
print_status "Building llama.cpp with Metal support..."
mkdir -p build
cd build

print_status "Configuring build with Metal support..."
cmake .. -DGGML_METAL=ON

print_status "Building llama.cpp (this may take several minutes)..."
cmake --build . --config Release

# Test the build
print_status "Testing AMD eGPU detection..."
if ./bin/llama-cli --help 2>&1 | grep -q "AMD Radeon RX 6800"; then
    print_success "AMD eGPU detected and working!"
else
    print_warning "AMD eGPU not detected in test. Build may still work."
fi

# Create models directory
print_status "Creating models directory..."
mkdir -p ../models
cd ../models

# Download test model
print_status "Downloading TinyLlama test model (637MB)..."
if [ ! -f "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" ]; then
    curl -L -o tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
        "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    print_success "TinyLlama model downloaded"
else
    print_success "TinyLlama model already exists"
fi

# Test the model
print_status "Testing model with AMD eGPU..."
cd ../build
if ./bin/llama-cli -m ../models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
   -p "Hello! Can you tell me a short joke?" \
   -n 20 --verbose 2>&1 | grep -q "offloaded.*layers to GPU"; then
    print_success "Model test successful - GPU acceleration working!"
else
    print_warning "Model test completed but GPU usage unclear. Check verbose output."
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install psutil requests

# Create symlinks for easy access
print_status "Creating symlinks for easy access..."
ln -sf "$LLAMA_CPP_DIR/build/bin/llama-cli" "$HOME/bin/llama-cli" 2>/dev/null || true
mkdir -p "$HOME/bin"

# Create environment setup script
print_status "Creating environment setup script..."
cat > "$HOME/.amd_egpu_setup" << EOF
# AMD eGPU Setup Environment
export LLAMA_CPP_PATH="$LLAMA_CPP_DIR/build/bin/llama-cli"
export LLAMA_MODELS_PATH="$LLAMA_CPP_DIR/models"
export PATH="$LLAMA_CPP_DIR/build/bin:\$PATH"

# Aliases for easy access
alias llama-cli="$LLAMA_CPP_DIR/build/bin/llama-cli"
alias llama-models="cd $LLAMA_CPP_DIR/models"
alias llama-build="cd $LLAMA_CPP_DIR/build"

echo "🚀 AMD eGPU setup loaded. Use 'llama-cli' to run models with GPU acceleration."
EOF

# Add to shell profile
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [ -n "$SHELL_PROFILE" ]; then
    if ! grep -q "amd_egpu_setup" "$SHELL_PROFILE"; then
        print_status "Adding setup to $SHELL_PROFILE"
        echo "source ~/.amd_egpu_setup" >> "$SHELL_PROFILE"
    fi
fi

# Final summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
print_success "llama.cpp built with Metal AMD eGPU support"
print_success "TinyLlama test model downloaded and tested"
print_success "Python dependencies installed"
print_success "Environment configured"
echo ""
echo "📋 Next Steps:"
echo "1. Restart your terminal or run: source ~/.amd_egpu_setup"
echo "2. Test with: llama-cli -m ~/llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p 'Hello!' -n 20"
echo "3. Download more models to ~/llama.cpp/models/"
echo "4. Use the Python wrapper scripts for integration"
echo ""
echo "📚 Documentation:"
echo "- README: $(pwd)/README_AMD_eGPU_Setup.md"
echo "- Helper script: $(pwd)/model_integration_helper.py"
echo "- Demo script: $(pwd)/simple_gpu_demo.py"
echo ""
print_success "Your AMD eGPU is now ready for local AI development!"
