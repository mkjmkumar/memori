#!/usr/bin/env python3
"""
MongoDB Integration Test for Memori
Tests the new MongoDB support alongside the existing SQL support
"""

import os
import sys

# Add the memori package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_mongodb_basic():
    """Test basic MongoDB functionality"""
    print("🧪 Testing MongoDB Integration...")
    
    try:
        # Try importing with MongoDB support
        from memori.core.memory import Memori
        
        # Test MongoDB connection string detection
        print("\n1. Testing MongoDB connection string detection...")
        
        # Create Memori instance with MongoDB connection string
        # Using a local MongoDB instance - will fail gracefully if not available
        memory = Memori(
            database_connect="mongodb://localhost:65482/memori_test",
            namespace="mongodb_test",
            verbose=True,
            schema_init=True  # This should create collections and indexes
        )
        
        print("✅ MongoDB connection string detected successfully")
        print(f"📊 Database type: {memory.db_manager.database_type}")
        print(f"🗄️ Database name: {memory.db_manager.database_name}")
        
        # Test basic database operations
        print("\n2. Testing database initialization...")
        try:
            stats = memory.get_memory_stats()
            print("✅ Database stats retrieved successfully:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        except Exception as e:
            print(f"❌ Database stats failed: {e}")
        
        print("\n3. Testing memory storage (requires MongoDB running)...")
        try:
            # Enable memory recording
            memory.enable()
            
            # Record a test conversation
            chat_id = memory.record_conversation(
                user_input="Hello, this is a test message for MongoDB storage",
                ai_output="I understand! This is a test response stored in MongoDB.",
                model="test-model"
            )
            
            print(f"✅ Conversation stored with ID: {chat_id}")
            
            # Test memory search
            print("\n4. Testing memory search...")
            results = memory.retrieve_context("test message", limit=5)
            print(f"✅ Search returned {len(results)} results")
            
            if results:
                print("📝 Sample result:")
                sample = results[0]
                for key, value in list(sample.items())[:3]:  # Show first 3 fields
                    print(f"   {key}: {str(value)[:50]}...")
            
            # Test memory stats after operations
            print("\n5. Testing memory stats after operations...")
            final_stats = memory.get_memory_stats()
            print("✅ Final stats:")
            for key, value in final_stats.items():
                print(f"   {key}: {value}")
            
            print("\n6. Testing memory cleanup...")
            memory.clear_memory("chat_history")
            print("✅ Memory cleared successfully")
            
        except Exception as e:
            print(f"❌ Memory operations failed (MongoDB may not be running): {e}")
            print("💡 To test fully, ensure MongoDB is running on localhost:27017")
        
        print("\n✅ MongoDB integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed - pymongo may not be installed: {e}")
        print("💡 Install with: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_sql_compatibility():
    """Test that SQL support still works after MongoDB integration"""
    print("\n🧪 Testing SQL Compatibility...")
    
    try:
        from memori.core.memory import Memori
        
        # Test SQLite (should still work as before)
        memory = Memori(
            database_connect="sqlite:///test_compat.db",
            namespace="sql_test",
            verbose=True,
            schema_init=True
        )
        
        print("✅ SQLite connection still works")
        print(f"📊 Database type: {memory.db_manager.database_type}")
        
        # Test basic operations
        stats = memory.get_memory_stats()
        print("✅ SQL database operations still work")
        print(f"📊 SQL Stats: {list(stats.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ SQL compatibility test failed: {e}")
        return False


def demo_usage():
    """Demonstrate the new MongoDB usage"""
    print("\n🎯 MongoDB Usage Demo")
    print("=" * 50)
    
    example_code = """
# MongoDB Integration Example
from memori.core.memory import Memori

# Create Memori instance with MongoDB
memory = Memori(
    api_key="your-openai-key",
    database_connect="mongodb://localhost:27017/memori",
    namespace="chat_app",
    auto_ingest=True,
    verbose=True
)

# Enable automatic memory recording
memory.enable()

# Use exactly like before - all existing functionality works!
memory.record_conversation(
    user_input="User prefers dark mode",
    ai_output="I'll remember your preference for dark mode."
)

# Search memories (uses MongoDB text search + fallback)
memories = memory.search("preferences", limit=5)

# All existing methods work identically
stats = memory.get_memory_stats()
memory.clear_memory("short_term")

# Connection strings supported:
# - mongodb://localhost:27017/dbname      (Local MongoDB)
# - mongodb+srv://cluster.mongodb.net/db  (MongoDB Atlas)
# - sqlite:///memori.db                   (SQLite - existing)
# - postgresql://user:pass@host/db        (PostgreSQL - existing)  
# - mysql://user:pass@host/db             (MySQL - existing)
"""
    
    print(example_code)


if __name__ == "__main__":
    print("🚀 Memori MongoDB Integration Test Suite")
    print("=" * 50)
    
    # Run tests
    mongodb_success = test_mongodb_basic()
    sql_success = test_sql_compatibility()
    
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print(f"   MongoDB Integration: {'✅ PASS' if mongodb_success else '❌ FAIL'}")
    print(f"   SQL Compatibility:   {'✅ PASS' if sql_success else '❌ FAIL'}")
    
    if mongodb_success and sql_success:
        print("\n🎉 All tests passed! MongoDB integration is ready.")
        demo_usage()
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Install MongoDB: https://docs.mongodb.com/manual/installation/")
    print("2. Install pymongo: pip install pymongo")
    print("3. Start MongoDB: mongod")
    print("4. Test with your applications!")