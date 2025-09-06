#!/usr/bin/env python3
"""
MongoDB + OpenAI + Memori Integration Example

This example demonstrates how to build an AI assistant with persistent memory
using MongoDB for storage and OpenAI for language processing.

Prerequisites:
1. MongoDB running locally or MongoDB Atlas account
2. OpenAI API key
3. Install required packages: pip install memori openai pymongo

Usage:
    export OPENAI_API_KEY="your-api-key"
    export MONGODB_URI="mongodb://localhost:27017/memori" # or your MongoDB Atlas URI
    python mongodb_openai_example.py
"""

import os
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
from memori import Memori

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/memori")
MODEL_NAME = "gpt-4o-mini"  # or "gpt-3.5-turbo" for lower cost

def setup_memory_system():
    """
    Initialize the memory system with MongoDB backend
    """
    memory = Memori(
        api_type="openai",
        api_key=OPENAI_API_KEY,
        database_connect=MONGODB_URI,
        auto_ingest=True,           # Automatically store important memories
        conscious_ingest=True,       # Process memories with AI analysis
        verbose=True,               # Show debug output
        namespace="openai_assistant" # Namespace for this assistant
    )
    
    # Enable memory storage
    memory.enable_memory = True
    
    print(f"✅ Memory system initialized with MongoDB")
    print(f"📦 Database: {MONGODB_URI}")
    print(f"🤖 Model: {MODEL_NAME}")
    
    return memory

def create_openai_assistant(memory: Memory):
    """
    Create an OpenAI assistant with memory capabilities
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    class MemoryAssistant:
        def __init__(self, memory_system: Memori, openai_client: OpenAI):
            self.memory = memory_system
            self.client = openai_client
            self.conversation_history = []
            
        def chat(self, user_input: str) -> str:
            """
            Process user input with memory context
            """
            # Search relevant memories
            relevant_memories = self._search_memories(user_input)
            
            # Build context from memories
            memory_context = self._format_memories(relevant_memories)
            
            # Create system prompt with memory context
            system_prompt = f"""You are a helpful AI assistant with persistent memory.
            
Previous relevant memories:
{memory_context if memory_context else "No relevant memories found."}

Use the above memories to provide personalized and contextual responses.
Remember important information from this conversation for future interactions."""
            
            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history (last 5 exchanges)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_response = response.choices[0].message.content
            
            # Store the interaction in memory
            self._store_interaction(user_input, assistant_response)
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        
        def _search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
            """
            Search for relevant memories based on the query
            """
            try:
                # Use memori's built-in search
                search_results = self.memory.search(
                    query=query,
                    namespace="openai_assistant",
                    limit=limit
                )
                return search_results if search_results else []
            except Exception as e:
                print(f"Memory search error: {e}")
                return []
        
        def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
            """
            Format memories for inclusion in the prompt
            """
            if not memories:
                return ""
            
            formatted = []
            for memory in memories:
                # Extract relevant information from memory
                if isinstance(memory, dict):
                    content = memory.get("searchable_content", "")
                    summary = memory.get("summary", "")
                    timestamp = memory.get("created_at", "")
                    importance = memory.get("importance_score", 0.5)
                    
                    if content or summary:
                        formatted.append(
                            f"- [{timestamp[:10] if timestamp else 'Unknown date'}] "
                            f"(Importance: {importance:.2f}): {summary or content[:100]}"
                        )
            
            return "\n".join(formatted[:5])  # Limit to top 5 memories
        
        def _store_interaction(self, user_input: str, assistant_response: str):
            """
            Store the interaction as a memory
            """
            try:
                # Create memory entry
                interaction_text = f"User asked: {user_input}\nAssistant responded: {assistant_response}"
                
                # Let memori determine importance and store if significant
                self.memory.add(
                    text=interaction_text,
                    metadata={
                        "type": "conversation",
                        "user_input": user_input,
                        "assistant_response": assistant_response,
                        "timestamp": datetime.now().isoformat(),
                        "model": MODEL_NAME
                    }
                )
                
                print(f"💾 Memory stored: {user_input[:50]}...")
                
            except Exception as e:
                print(f"Failed to store memory: {e}")
    
    return MemoryAssistant(memory, client)

def run_example_conversation():
    """
    Run an example conversation to demonstrate the memory system
    """
    print("\n" + "="*60)
    print("🚀 MongoDB + OpenAI + Memori Integration Demo")
    print("="*60)
    
    # Initialize memory system
    memory = setup_memory_system()
    
    # Create assistant
    assistant = create_openai_assistant(memory)
    
    # Example conversations
    example_conversations = [
        "Hi! My name is Alice and I love Python programming.",
        "I'm working on a machine learning project using TensorFlow.",
        "What's my name and what am I interested in?",
        "Can you suggest some Python libraries that might help with my project?",
        "I also enjoy hiking on weekends. Last week I went to Mount Tamalpais.",
        "Based on what you know about me, what would be a good weekend activity?"
    ]
    
    print("\n📝 Starting example conversation...\n")
    
    for user_input in example_conversations:
        print(f"\n👤 User: {user_input}")
        response = assistant.chat(user_input)
        print(f"🤖 Assistant: {response}")
        print("-" * 40)
    
    # Show memory statistics
    print("\n📊 Memory Statistics:")
    try:
        stats = memory.get_stats()
        print(f"Total memories stored: {stats.get('total_memories', 0)}")
        print(f"Namespaces: {stats.get('namespaces', [])}")
    except:
        print("Unable to retrieve statistics")

def interactive_chat():
    """
    Run an interactive chat session
    """
    print("\n" + "="*60)
    print("💬 Interactive Chat with Memory (MongoDB + OpenAI)")
    print("="*60)
    print("Type 'quit' to exit, 'memories' to see stored memories\n")
    
    # Initialize
    memory = setup_memory_system()
    assistant = create_openai_assistant(memory)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'memories':
                # Show recent memories
                print("\n📚 Recent Memories:")
                memories = assistant._search_memories("", limit=10)
                for i, mem in enumerate(memories, 1):
                    summary = mem.get("summary", mem.get("searchable_content", ""))[:100]
                    print(f"{i}. {summary}...")
                continue
            
            elif user_input:
                response = assistant.chat(user_input)
                print(f"\n🤖 Assistant: {response}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """
    Main function to run the example
    """
    import sys
    
    # Check for API key
    if OPENAI_API_KEY == "your-api-key-here":
        print("⚠️  Please set your OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-actual-api-key'")
        sys.exit(1)
    
    # Check for MongoDB URI
    if not MONGODB_URI:
        print("⚠️  Please set your MONGODB_URI environment variable")
        print("   export MONGODB_URI='mongodb://localhost:27017/memori'")
        sys.exit(1)
    
    # Run example or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
    else:
        run_example_conversation()
        print("\n💡 Tip: Run with --interactive flag for interactive chat")
        print("   python mongodb_openai_example.py --interactive")

if __name__ == "__main__":
    main()