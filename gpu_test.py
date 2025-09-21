import os
import time
from litellm import completion

# Set GPU environment
os.environ["OLLAMA_GPU_OVERHEAD"] = "0"
os.environ["OLLAMA_MAX_LOADED_MODELS"] = "1"
os.environ["HIP_VISIBLE_DEVICES"] = "0"

def test_gpu_acceleration():
    print("🚀 Testing GPU Acceleration...")
    print("=" * 50)
    
    models_to_test = [
        ("tinyllama:latest", "simple"),
        ("llama3.2:3b", "medium"), 
        ("granite-code:34b", "complex")
    ]
    
    for model_name, complexity in models_to_test:
        print(f"\n🧪 Testing {model_name} ({complexity})")
        print("-" * 40)
        
        test_question = f"How does video processing work on a system with {complexity} complexity?"
        
        start_time = time.time()
        
        try:
            response = completion(
                model=f"ollama/{model_name}",
                messages=[{"role": "user", "content": test_question}],
                max_tokens=200
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ Response time: {duration:.2f} seconds")
            print(f"✅ GPU Acceleration: {'Enabled' if duration < 2.0 else 'CPU Fallback'}")
            
            # Show first 100 characters
            content = response.choices[0].message.content
            print(f"📝 Response: {content[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print("🎯 GPU Test Complete!")

if __name__ == "__main__":
    test_gpu_acceleration()