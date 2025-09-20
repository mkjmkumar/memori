#!/usr/bin/env python3
"""
Test script to demonstrate memori with Ollama and AMD eGPU
This shows how to use local models with memory persistence to save costs
"""

import os
import time
from memori import Memori
from memori.core.providers import ProviderConfig

def main():
    print("🚀 Testing Memori with Ollama and AMD eGPU")
    print("=" * 50)
    
    # Create Ollama provider configuration
    ollama_provider = ProviderConfig.from_custom(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Ollama doesn't require an API key
        model="tinyllama"  # Using the model we just tested
    )
    
    # Initialize memori with Ollama
    print("📝 Initializing Memori with Ollama...")
    memori = Memori(
        database_connect="sqlite:///ollama_memori_test.db",
        conscious_ingest=True,  # Short-term working memory
        auto_ingest=True,       # Dynamic search
        verbose=True,
        provider_config=ollama_provider,
    )
    
    # Create client using the provider config
    client = ollama_provider.create_client()
    
    print("🧠 Enabling memory tracking...")
    memori.enable()
    
    print("\n💬 Starting conversation with memory...")
    print("Type 'exit' to quit, 'stats' to see memory statistics")
    print("-" * 50)
    
    conversation_count = 0
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == 'stats':
                stats = memori.get_memory_stats()
                print(f"\n📊 Memory Statistics:")
                print(f"   Long-term memories: {stats.get('long_term_count', 0)}")
                print(f"   Chat history entries: {stats.get('chat_history_count', 0)}")
                continue
            
            conversation_count += 1
            print(f"\n🤖 AI (conversation #{conversation_count}): ", end="", flush=True)
            
            # Make API call - memori automatically records this
            start_time = time.time()
            response = client.chat.completions.create(
                model="tinyllama",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=100,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            end_time = time.time()
            
            print(ai_response)
            print(f"\n⏱️  Response time: {end_time - start_time:.2f} seconds")
            
            # Show memory context if available
            if conversation_count > 1:
                try:
                    context = memori.retrieve_context(user_input, limit=2)
                    if context:
                        print(f"\n🧠 Memory context: {len(context)} relevant memories found")
                except Exception as e:
                    print(f"\n⚠️  Memory retrieval: {e}")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Make sure Ollama is running: 'ollama serve'")
            continue
    
    # Final statistics
    try:
        stats = memori.get_memory_stats()
        print(f"\n📊 Final Memory Statistics:")
        print(f"   Long-term memories: {stats.get('long_term_count', 0)}")
        print(f"   Chat history entries: {stats.get('chat_history_count', 0)}")
        print(f"   Total conversations: {conversation_count}")
    except Exception as e:
        print(f"Could not retrieve final stats: {e}")
    
    print("\n✅ Test completed!")
    print("💾 Database saved to: ollama_memori_test.db")
    print("🔄 Next time you run this, memori will remember your conversations!")

if __name__ == "__main__":
    main()
