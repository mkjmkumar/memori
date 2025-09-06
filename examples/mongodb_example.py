"""
MongoDB Integration Example for Memori
Demonstrates how to use MongoDB as a backend for memory storage
"""

import asyncio
import json
from typing import List, Dict, Any

from memori.config.settings import MemoriSettings, DatabaseType
from memori.database.connectors.mongodb_connector import MongoDBConnector
from memori.database.adapters.mongodb_adapter import MongoDBAdapter
from memori.database.search.mongodb_search_adapter import MongoDBSearchAdapter


def create_mongodb_settings(connection_string: str = None) -> MemoriSettings:
    """Create Memori settings configured for MongoDB"""
    
    # Default MongoDB connection strings for different scenarios
    if not connection_string:
        # Local MongoDB instance
        connection_string = "mongodb://localhost:27017/memori"
        
        # Uncomment for MongoDB Atlas (replace with your connection string)
        # connection_string = "mongodb+srv://username:password@cluster.mongodb.net/memori"
    
    settings = MemoriSettings()
    settings.database.database_type = DatabaseType.MONGODB
    settings.database.connection_string = connection_string
    
    return settings


def setup_mongodb_backend(settings: MemoriSettings) -> tuple:
    """Setup MongoDB backend components"""
    
    # Create MongoDB connector
    connector = MongoDBConnector(settings.database.connection_string)
    
    # Test connection
    if not connector.test_connection():
        raise ConnectionError("Failed to connect to MongoDB")
    
    # Initialize schema (creates collections and indexes)
    connector.initialize_schema()
    
    # Create adapter for memory operations
    adapter = MongoDBAdapter(connector)
    
    # Create search adapter
    search_adapter = MongoDBSearchAdapter(connector)
    
    # Create search indexes for optimal performance
    search_adapter.create_search_indexes()
    
    return connector, adapter, search_adapter


def demo_basic_memory_operations(adapter: MongoDBAdapter):
    """Demonstrate basic CRUD operations with MongoDB"""
    print("\n=== Basic Memory Operations Demo ===")
    
    # Store a short-term memory
    short_memory = {
        "processed_data": {"content": "User prefers dark mode in applications"},
        "importance_score": 0.7,
        "category_primary": "user_preference",
        "namespace": "demo_session",
        "searchable_content": "user interface preferences dark mode applications",
        "summary": "User prefers dark mode UI",
        "retention_type": "short_term"
    }
    
    memory_id = adapter.store_short_term_memory(short_memory)
    print(f"Stored short-term memory: {memory_id}")
    
    # Store a long-term memory
    long_memory = {
        "processed_data": {"content": "User is working on a Python machine learning project using scikit-learn"},
        "importance_score": 0.8,
        "category_primary": "project_context",
        "namespace": "demo_session",
        "searchable_content": "Python machine learning scikit-learn project development",
        "summary": "User working on Python ML project",
        "classification": "project_work",
        "topic": "machine learning",
        "is_skill_knowledge": True,
        "is_current_project": True
    }
    
    ml_memory_id = adapter.store_long_term_memory(long_memory)
    print(f"Stored long-term memory: {ml_memory_id}")
    
    # Retrieve memories
    short_memories = adapter.get_short_term_memories(namespace="demo_session")
    print(f"Retrieved {len(short_memories)} short-term memories")
    
    long_memories = adapter.get_long_term_memories(namespace="demo_session")
    print(f"Retrieved {len(long_memories)} long-term memories")
    
    # Update a memory
    updates = {"importance_score": 0.9, "access_count": 5}
    success = adapter.update_long_term_memory(ml_memory_id, updates)
    print(f"Memory update successful: {success}")
    
    return memory_id, ml_memory_id


def demo_search_operations(search_adapter: MongoDBSearchAdapter):
    """Demonstrate search capabilities"""
    print("\n=== Search Operations Demo ===")
    
    # Text search
    text_results = search_adapter.execute_fulltext_search(
        query="Python machine learning",
        namespace="demo_session",
        limit=5
    )
    print(f"Text search found {len(text_results)} results")
    for result in text_results:
        print(f"  - {result.get('summary', 'No summary')} (score: {result.get('importance_score', 0)})")
    
    # Category-filtered search
    preference_results = search_adapter.execute_fulltext_search(
        query="user preferences",
        namespace="demo_session",
        category_filter=["user_preference"],
        limit=5
    )
    print(f"Category-filtered search found {len(preference_results)} results")
    
    # Fallback regex search (when text search isn't available)
    fallback_results = search_adapter.execute_fallback_search(
        query="dark mode",
        namespace="demo_session",
        limit=5
    )
    print(f"Fallback search found {len(fallback_results)} results")


def demo_vector_search(search_adapter: MongoDBSearchAdapter):
    """Demonstrate vector search (Atlas only)"""
    print("\n=== Vector Search Demo ===")
    
    if search_adapter._check_vector_search_available():
        print("Vector search is available!")
        
        # Example: search with a dummy embedding vector
        # In real usage, you'd generate this from your embedding model
        dummy_vector = [0.1] * 1536  # OpenAI ada-002 dimensions
        
        try:
            vector_results = search_adapter.execute_vector_search(
                query_vector=dummy_vector,
                namespace="demo_session",
                limit=5,
                similarity_threshold=0.5
            )
            print(f"Vector search found {len(vector_results)} results")
            for result in vector_results:
                print(f"  - {result.get('summary', 'No summary')} (vector score: {result.get('vector_score', 0)})")
        except Exception as e:
            print(f"Vector search failed (may need proper index setup): {e}")
            
        # Hybrid search combining text and vector
        try:
            hybrid_results = search_adapter.execute_hybrid_search(
                query="machine learning Python",
                query_vector=dummy_vector,
                namespace="demo_session",
                limit=5,
                text_weight=0.6,
                vector_weight=0.4
            )
            print(f"Hybrid search found {len(hybrid_results)} results")
            for result in hybrid_results:
                print(f"  - {result.get('summary', 'No summary')} (combined score: {result.get('combined_score', 0)})")
        except Exception as e:
            print(f"Hybrid search failed: {e}")
    else:
        print("Vector search not available (requires MongoDB Atlas with vector search index)")


def demo_batch_operations(adapter: MongoDBAdapter):
    """Demonstrate batch operations for efficiency"""
    print("\n=== Batch Operations Demo ===")
    
    # Create multiple memories for batch insertion
    batch_memories = []
    for i in range(5):
        memory = {
            "processed_data": {"content": f"Batch memory {i+1} about programming concepts"},
            "importance_score": 0.5 + (i * 0.1),
            "category_primary": "learning",
            "namespace": "demo_session",
            "searchable_content": f"programming concept {i+1} learning development",
            "summary": f"Programming concept {i+1}",
            "classification": "educational"
        }
        batch_memories.append(memory)
    
    # Batch store long-term memories
    memory_ids = adapter.batch_store_memories(batch_memories, memory_type="long_term")
    print(f"Batch stored {len(memory_ids)} long-term memories")
    
    # Get memory statistics
    stats = adapter.get_memory_stats(namespace="demo_session")
    print(f"Memory statistics: {json.dumps(stats, indent=2, default=str)}")


def demo_chat_history(adapter: MongoDBAdapter):
    """Demonstrate chat history storage"""
    print("\n=== Chat History Demo ===")
    
    # Store some chat interactions
    chat_interactions = [
        {
            "chat_id": "chat_001",
            "user_input": "What's the best way to learn machine learning?",
            "ai_output": "I recommend starting with Python and scikit-learn, then moving to more advanced frameworks like TensorFlow or PyTorch.",
            "model": "gpt-4",
            "session_id": "session_001",
            "namespace": "demo_session",
            "tokens_used": 45
        },
        {
            "chat_id": "chat_002", 
            "user_input": "Can you explain neural networks?",
            "ai_output": "Neural networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes that can learn patterns in data.",
            "model": "gpt-4",
            "session_id": "session_001",
            "namespace": "demo_session",
            "tokens_used": 52
        }
    ]
    
    for interaction in chat_interactions:
        chat_id = adapter.store_chat_interaction(**interaction)
        print(f"Stored chat interaction: {chat_id}")
    
    # Retrieve chat history
    history = adapter.get_chat_history(namespace="demo_session", session_id="session_001")
    print(f"Retrieved {len(history)} chat history entries")
    for entry in history:
        print(f"  - {entry['user_input'][:50]}...")


def demo_mongodb_capabilities(connector: MongoDBConnector):
    """Show MongoDB-specific capabilities"""
    print("\n=== MongoDB Capabilities ===")
    
    # Get database information
    db_info = connector.get_database_info()
    print("Database Information:")
    for key, value in db_info.items():
        print(f"  {key}: {value}")
    
    # Show search capabilities
    from memori.database.search.mongodb_search_adapter import MongoDBSearchAdapter
    search_adapter = MongoDBSearchAdapter(connector)
    capabilities = search_adapter.get_search_capabilities()
    print("\nSearch Capabilities:")
    for key, value in capabilities.items():
        print(f"  {key}: {value}")


def cleanup_demo_data(adapter: MongoDBAdapter):
    """Clean up demo data"""
    print("\n=== Cleanup Demo Data ===")
    
    # In a real application, you might want to clean up test data
    # For this demo, we'll just show how to get statistics
    stats = adapter.get_memory_stats(namespace="demo_session")
    print(f"Demo created {stats.get('short_term_count', 0)} short-term and {stats.get('long_term_count', 0)} long-term memories")
    
    # Cleanup expired memories
    expired_count = adapter.cleanup_expired_memories(namespace="demo_session")
    print(f"Cleaned up {expired_count} expired memories")


def main():
    """Main demonstration function"""
    print("MongoDB Integration Example for Memori")
    print("=====================================")
    
    try:
        # Create MongoDB settings
        # Modify the connection string as needed for your setup
        connection_string = "mongodb://localhost:27017/memori_demo"
        settings = create_mongodb_settings(connection_string)
        
        print(f"Connecting to MongoDB: {connection_string}")
        
        # Setup MongoDB backend
        connector, adapter, search_adapter = setup_mongodb_backend(settings)
        
        print(f"Successfully connected to MongoDB!")
        
        # Run demonstrations
        demo_mongodb_capabilities(connector)
        demo_basic_memory_operations(adapter)
        demo_search_operations(search_adapter)
        demo_vector_search(search_adapter)
        demo_batch_operations(adapter)
        demo_chat_history(adapter)
        cleanup_demo_data(adapter)
        
        print("\n=== Demo Complete ===")
        print("MongoDB integration is working successfully!")
        
    except ImportError as e:
        if "pymongo" in str(e):
            print("Error: pymongo is required for MongoDB support.")
            print("Install it with: pip install pymongo")
        else:
            print(f"Import error: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
        print("Make sure MongoDB is running and accessible.")
        print("For local MongoDB: brew install mongodb/brew/mongodb-community (macOS) or follow MongoDB installation guide")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


def mongodb_atlas_example():
    """Example configuration for MongoDB Atlas"""
    print("\nMongoDB Atlas Configuration Example:")
    print("=====================================")
    
    atlas_connection_examples = {
        "Standard Atlas Connection": "mongodb+srv://username:password@cluster-name.abcde.mongodb.net/memori",
        "Atlas with SSL": "mongodb+srv://username:password@cluster-name.abcde.mongodb.net/memori?retryWrites=true&w=majority",
        "Atlas with specific options": "mongodb+srv://username:password@cluster-name.abcde.mongodb.net/memori?retryWrites=true&w=majority&appName=Memori"
    }
    
    for name, connection in atlas_connection_examples.items():
        print(f"\n{name}:")
        print(f"  {connection}")
    
    print("\nVector Search Setup (Atlas only):")
    print("1. Create a vector search index in Atlas UI or via API")
    print("2. Index name: 'vector_search_index'")  
    print("3. Field path: 'embedding_vector'")
    print("4. Vector type: 'vector'")
    print("5. Dimensions: 1536 (for OpenAI ada-002 embeddings)")
    print("6. Similarity: 'cosine'")


if __name__ == "__main__":
    main()
    mongodb_atlas_example()