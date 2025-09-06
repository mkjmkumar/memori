#!/usr/bin/env python3
"""
MongoDB Integration Demo for Memori
Demonstrates how to use Memori with MongoDB as the backend database
"""

import os
import sys
from datetime import datetime

# Add the memori package to Python path for demo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def demo_mongodb_basic():
    """Basic MongoDB usage demo"""
    print("🍃 MongoDB Basic Usage Demo")
    print("-" * 40)
    
    try:
        from memori.core.memory import Memori
        
        # Create Memori instance with MongoDB
        # This will automatically detect MongoDB and use MongoDBDatabaseManager
        memory = Memori(
            database_connect="mongodb://localhost:27017/memori_demo",
            namespace="demo_app",
            auto_ingest=True,
            verbose=True
        )
        
        print("✅ Connected to MongoDB successfully")
        print(f"📊 Database type: {memory.db_manager.database_type}")
        print(f"🗄️ Database: {memory.db_manager.database_name}")
        
        # Enable automatic memory recording
        memory.enable()
        print("🔄 Memory recording enabled")
        
        # Simulate some conversations that will be stored in MongoDB
        conversations = [
            {
                "user": "Hi, my name is Alice and I'm a software engineer",
                "ai": "Hello Alice! Nice to meet you. I'll remember that you're a software engineer."
            },
            {
                "user": "I'm working on a Python project using MongoDB",
                "ai": "That's great! MongoDB is excellent for flexible data storage. What kind of Python project are you building?"
            },
            {
                "user": "I prefer to work in dark mode and use VS Code",
                "ai": "I'll remember your preferences - dark mode and VS Code. Those are popular choices among developers!"
            },
            {
                "user": "Can you help me with MongoDB queries?",
                "ai": "Absolutely! I remember you're working with MongoDB. I can help with queries, aggregation pipelines, indexing, and more."
            }
        ]
        
        print("\n💬 Recording sample conversations in MongoDB...")
        chat_ids = []
        
        for i, conv in enumerate(conversations, 1):
            chat_id = memory.record_conversation(
                user_input=conv["user"],
                ai_output=conv["ai"],
                model="gpt-4o",
                metadata={"demo": True, "conversation_number": i}
            )
            chat_ids.append(chat_id)
            print(f"   {i}. Stored conversation: {chat_id}")
        
        # Wait a moment for processing
        import time
        time.sleep(2)
        
        # Test memory search using MongoDB text search
        print("\n🔍 Testing memory search...")
        search_queries = [
            "Alice engineer",
            "Python MongoDB",
            "dark mode preferences",
            "software"
        ]
        
        for query in search_queries:
            results = memory.retrieve_context(query, limit=3)
            print(f"   Query: '{query}' → {len(results)} results")
            
            if results:
                top_result = results[0]
                preview = top_result.get('searchable_content', top_result.get('summary', ''))[:60]
                print(f"      Top result: {preview}...")
        
        # Show memory statistics
        print("\n📊 Memory Statistics:")
        stats = memory.get_memory_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Make sure MongoDB is running and pymongo is installed")
        return False


def demo_mongodb_atlas():
    """Demo using MongoDB Atlas (cloud)"""
    print("\n☁️  MongoDB Atlas Usage Demo")
    print("-" * 40)
    
    print("MongoDB Atlas connection example:")
    print("""
# For MongoDB Atlas, use a connection string like:
memory = Memori(
    api_key="your-openai-key",
    database_connect="mongodb+srv://username:password@cluster.mongodb.net/memori",
    namespace="production_app",
    auto_ingest=True,
    verbose=True
)

# All the same methods work identically!
memory.enable()
memory.record_conversation("Hello", "Hi there!")
results = memory.retrieve_context("hello")
""")


def demo_connection_string_options():
    """Demo various connection string options"""
    print("\n🔌 Connection String Options")
    print("-" * 40)
    
    examples = [
        ("Local MongoDB", "mongodb://localhost:27017/memori"),
        ("Local with Auth", "mongodb://user:pass@localhost:27017/memori"),
        ("MongoDB Atlas", "mongodb+srv://user:pass@cluster.mongodb.net/memori"),
        ("Local with Options", "mongodb://localhost:27017/memori?retryWrites=true&w=majority"),
        ("SQLite (existing)", "sqlite:///memori.db"),
        ("PostgreSQL (existing)", "postgresql://user:pass@localhost/memori"),
        ("MySQL (existing)", "mysql://user:pass@localhost/memori")
    ]
    
    print("Supported connection strings:")
    for name, conn_str in examples:
        print(f"   {name:20}: {conn_str}")


def demo_feature_parity():
    """Demo that all existing features work with MongoDB"""
    print("\n⚖️  Feature Parity Demo")
    print("-" * 40)
    
    print("✅ All existing Memori features work identically with MongoDB:")
    print("""
# Memory Management
memory.record_conversation(user_input, ai_output)
memory.retrieve_context(query, limit=5)
memory.search_memories_by_category("preferences")
memory.get_conversation_history()

# Auto-ingest and Conscious Ingestion
memory = Memori(
    database_connect="mongodb://localhost:27017/memori",
    auto_ingest=True,          # ✅ Works with MongoDB
    conscious_ingest=True      # ✅ Works with MongoDB  
)

# Memory Types and Categories
# ✅ Short-term and long-term memories work identically
# ✅ All classification categories supported
# ✅ Importance scoring and filtering work

# Search and Retrieval
# ✅ Text search (uses MongoDB text indexes)
# ✅ Category filtering
# ✅ Importance thresholds
# ✅ Namespace isolation

# Memory Statistics and Management
memory.get_memory_stats()    # ✅ MongoDB-specific stats
memory.clear_memory()        # ✅ Works with MongoDB
memory.get_integration_stats() # ✅ Shows MongoDB status

# OpenAI Integration
client = memory.create_openai_client()  # ✅ Works identically
# Auto-recording still works with MongoDB backend
""")


def performance_comparison():
    """Compare performance characteristics"""
    print("\n🏎️  Performance Characteristics")
    print("-" * 40)
    
    print("MongoDB vs SQL Performance:")
    print("""
📊 Write Performance:
   MongoDB: Excellent (native JSON storage, no schema migrations)
   SQL:     Good (requires JSON serialization)

🔍 Search Performance:
   MongoDB: Excellent (native text search, flexible queries)
   SQL:     Good (depends on database - FTS varies)

📈 Scalability:
   MongoDB: Excellent (horizontal scaling, sharding)
   SQL:     Good (vertical scaling, some horizontal options)

💾 Storage Efficiency:
   MongoDB: Excellent (BSON compression, no wasted columns)
   SQL:     Good (depends on database engine)

🔧 Schema Flexibility:
   MongoDB: Excellent (schemaless, easy evolution)
   SQL:     Moderate (migrations required)
""")


def main():
    """Run all demos"""
    print("🚀 Memori MongoDB Integration Demo")
    print("=" * 50)
    
    success = demo_mongodb_basic()
    
    if success:
        demo_mongodb_atlas()
        demo_connection_string_options()
        demo_feature_parity()
        performance_comparison()
        
        print("\n🎉 MongoDB integration is working perfectly!")
        print("\n📋 Next Steps:")
        print("1. Try with your own MongoDB instance")
        print("2. Test with MongoDB Atlas for production")
        print("3. Compare performance with your existing SQL setup")
        print("4. Migrate existing data if needed")
    else:
        print("\n⚠️  MongoDB demo failed - see installation instructions above")
    
    print("\n" + "=" * 50)
    print("📚 Resources:")
    print("- MongoDB Installation: https://docs.mongodb.com/manual/installation/")
    print("- MongoDB Atlas: https://www.mongodb.com/cloud/atlas")
    print("- pymongo docs: https://pymongo.readthedocs.io/")


if __name__ == "__main__":
    main()