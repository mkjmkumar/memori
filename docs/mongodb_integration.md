# MongoDB Integration for Memori

This document provides comprehensive guidance on using MongoDB as a backend database for Memori memory storage.

## Overview

Memori now supports MongoDB as a database backend, offering several advantages:

- **Document-based storage**: Natural fit for JSON-based memory data
- **Horizontal scalability**: Easy scaling across multiple servers
- **Rich query capabilities**: Advanced search and aggregation features
- **Vector search support**: MongoDB Atlas provides native vector search capabilities
- **Schema flexibility**: No rigid schema requirements
- **Automatic sharding**: Built-in data distribution capabilities

## Prerequisites

### Software Requirements

1. **MongoDB Server** (Choose one):
   - Local MongoDB Community Server 4.0+
   - MongoDB Atlas (cloud service)
   - MongoDB Enterprise Server

2. **Python Dependencies**:
   ```bash
   pip install pymongo>=4.0.0
   ```

### MongoDB Installation

#### Local Installation

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

**Ubuntu/Debian:**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

**Windows:**
Download and install from the [official MongoDB website](https://www.mongodb.com/try/download/community).

#### MongoDB Atlas (Cloud)

1. Sign up at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a new cluster
3. Configure network access (IP whitelist)
4. Create database user credentials
5. Get your connection string

## Configuration

### Basic Configuration

```python
from memori.config.settings import MemoriSettings, DatabaseType

# Create settings for MongoDB
settings = MemoriSettings()
settings.database.database_type = DatabaseType.MONGODB
settings.database.connection_string = "mongodb://localhost:27017/memori"
```

### Connection String Examples

#### Local MongoDB
```python
# Basic local connection
connection_string = "mongodb://localhost:27017/memori"

# Local with authentication
connection_string = "mongodb://username:password@localhost:27017/memori"

# Local with options
connection_string = "mongodb://localhost:27017/memori?retryWrites=true&w=majority"
```

#### MongoDB Atlas
```python
# Standard Atlas connection
connection_string = "mongodb+srv://username:password@cluster-name.abcde.mongodb.net/memori"

# Atlas with specific options
connection_string = "mongodb+srv://username:password@cluster-name.abcde.mongodb.net/memori?retryWrites=true&w=majority&appName=Memori"
```

#### Authentication Options
```python
# Username/password authentication
connection_string = "mongodb://myuser:mypass@localhost:27017/memori"

# SSL/TLS connection
connection_string = "mongodb://username:password@localhost:27017/memori?ssl=true"

# Replica set connection
connection_string = "mongodb://host1:27017,host2:27017,host3:27017/memori?replicaSet=myReplicaSet"
```

## Usage

### Basic Setup

```python
from memori.database.connectors.mongodb_connector import MongoDBConnector
from memori.database.adapters.mongodb_adapter import MongoDBAdapter
from memori.database.search.mongodb_search_adapter import MongoDBSearchAdapter

# Create connector
connector = MongoDBConnector("mongodb://localhost:27017/memori")

# Test connection
if connector.test_connection():
    print("Connected to MongoDB!")

# Initialize schema (creates collections and indexes)
connector.initialize_schema()

# Create adapter for memory operations
adapter = MongoDBAdapter(connector)

# Create search adapter
search_adapter = MongoDBSearchAdapter(connector)
search_adapter.create_search_indexes()
```

### Memory Storage Operations

#### Storing Memories

```python
# Store short-term memory
short_memory = {
    "processed_data": {"content": "User prefers dark mode"},
    "importance_score": 0.7,
    "category_primary": "user_preference",
    "namespace": "user_session",
    "searchable_content": "user interface preferences dark mode",
    "summary": "User UI preferences"
}

memory_id = adapter.store_short_term_memory(short_memory)

# Store long-term memory
long_memory = {
    "processed_data": {"content": "User working on ML project"},
    "importance_score": 0.8,
    "category_primary": "project_context",
    "namespace": "user_session", 
    "searchable_content": "machine learning project Python scikit-learn",
    "summary": "ML project context",
    "classification": "project_work",
    "topic": "machine learning",
    "is_current_project": True
}

ml_memory_id = adapter.store_long_term_memory(long_memory)
```

#### Retrieving Memories

```python
# Get short-term memories
short_memories = adapter.get_short_term_memories(
    namespace="user_session",
    category_filter=["user_preference"],
    importance_threshold=0.5,
    limit=10
)

# Get long-term memories
long_memories = adapter.get_long_term_memories(
    namespace="user_session",
    classification_filter=["project_work"],
    importance_threshold=0.6,
    limit=20
)
```

#### Updating and Deleting

```python
# Update memory
updates = {"importance_score": 0.9, "access_count": 5}
success = adapter.update_long_term_memory(memory_id, updates)

# Delete memory
success = adapter.delete_short_term_memory(memory_id)
```

### Search Operations

#### Text Search

```python
# Full-text search across memories
results = search_adapter.execute_fulltext_search(
    query="machine learning Python",
    namespace="user_session",
    category_filter=["project_context"],
    limit=10
)

for result in results:
    print(f"Found: {result['summary']} (score: {result['importance_score']})")
```

#### Vector Search (MongoDB Atlas only)

```python
# Vector similarity search
query_vector = [0.1, 0.2, 0.3, ...]  # Your embedding vector

vector_results = search_adapter.execute_vector_search(
    query_vector=query_vector,
    namespace="user_session",
    similarity_threshold=0.7,
    limit=5
)

for result in vector_results:
    print(f"Similar: {result['summary']} (vector score: {result['vector_score']})")
```

#### Hybrid Search

```python
# Combine text and vector search
hybrid_results = search_adapter.execute_hybrid_search(
    query="machine learning project",
    query_vector=query_vector,
    namespace="user_session",
    limit=10,
    text_weight=0.6,
    vector_weight=0.4
)
```

### Batch Operations

```python
# Batch store multiple memories
memories = [
    {"processed_data": {...}, "importance_score": 0.6, ...},
    {"processed_data": {...}, "importance_score": 0.7, ...},
    # ... more memories
]

memory_ids = adapter.batch_store_memories(memories, memory_type="long_term")
```

### Chat History

```python
# Store chat interaction
chat_id = adapter.store_chat_interaction(
    chat_id="chat_001",
    user_input="What's the weather like?",
    ai_output="I don't have access to current weather data.",
    model="gpt-4",
    session_id="session_001",
    namespace="user_session",
    tokens_used=25
)

# Retrieve chat history
history = adapter.get_chat_history(
    namespace="user_session",
    session_id="session_001",
    limit=50
)
```

## Collections Schema

MongoDB uses three main collections:

### chat_history
Stores chat interactions between users and AI.
```javascript
{
  "_id": ObjectId,
  "chat_id": "string (unique)",
  "user_input": "string",
  "ai_output": "string",
  "model": "string",
  "timestamp": ISODate,
  "session_id": "string", 
  "namespace": "string",
  "tokens_used": "number",
  "metadata": "object"
}
```

### short_term_memory
Stores temporary memories with expiration.
```javascript
{
  "_id": ObjectId,
  "memory_id": "string (unique)",
  "chat_id": "string (optional)",
  "processed_data": "object",
  "importance_score": "number (0.0-1.0)",
  "category_primary": "string",
  "namespace": "string",
  "created_at": ISODate,
  "expires_at": "ISODate (optional)",
  "searchable_content": "string",
  "summary": "string",
  "is_permanent_context": "boolean"
  // ... other fields
}
```

### long_term_memory
Stores persistent memories with enhanced metadata.
```javascript
{
  "_id": ObjectId,
  "memory_id": "string (unique)",
  "processed_data": "object", 
  "importance_score": "number (0.0-1.0)",
  "category_primary": "string",
  "namespace": "string",
  "classification": "string",
  "topic": "string",
  "searchable_content": "string",
  "summary": "string",
  "is_user_context": "boolean",
  "is_preference": "boolean",
  "is_skill_knowledge": "boolean",
  "is_current_project": "boolean",
  "embedding_vector": "array<number> (optional)"
  // ... many other fields for enhanced classification
}
```

## Indexes and Performance

### Automatic Indexes

The MongoDB adapter automatically creates essential indexes:

- **Unique indexes**: `memory_id`, `chat_id`
- **Compound indexes**: `namespace + category + importance_score`
- **Text indexes**: `searchable_content + summary` for full-text search
- **Date indexes**: `created_at`, `expires_at`
- **Classification indexes**: Various fields for filtering

### Vector Search Index (Atlas only)

For vector similarity search, create a vector search index in MongoDB Atlas:

1. **Index Configuration**:
   - Collection: `long_term_memory`
   - Field path: `embedding_vector`
   - Index name: `vector_search_index`
   - Vector type: `vector`
   - Dimensions: `1536` (for OpenAI ada-002)
   - Similarity: `cosine`

2. **Atlas CLI Example**:
   ```bash
   atlas clusters search indexes create \
     --clusterName myCluster \
     --file vector-search-index.json
   ```

3. **Index JSON Definition**:
   ```json
   {
     "name": "vector_search_index",
     "type": "vectorSearch",
     "definition": {
       "fields": [
         {
           "path": "embedding_vector",
           "type": "vector",
           "similarity": "cosine",
           "dimensions": 1536
         }
       ]
     }
   }
   ```

## Advanced Features

### Atlas Vector Search

MongoDB Atlas provides native vector search capabilities:

```python
# Check if vector search is available
if search_adapter._check_vector_search_available():
    # Perform vector similarity search
    results = search_adapter.execute_vector_search(
        query_vector=embedding_vector,
        namespace="user_session",
        similarity_threshold=0.8,
        limit=10
    )
```

### Aggregation Pipelines

MongoDB's powerful aggregation framework can be used for complex queries:

```python
# Custom aggregation query
pipeline = [
    {"$match": {"namespace": "user_session"}},
    {"$group": {
        "_id": "$category_primary",
        "count": {"$sum": 1},
        "avg_importance": {"$avg": "$importance_score"}
    }},
    {"$sort": {"count": -1}}
]

results = connector.database["long_term_memory"].aggregate(pipeline)
```

### Geospatial Queries

If your memories include location data:

```python
# Store memory with location
memory_with_location = {
    "processed_data": {"content": "Meeting at coffee shop"},
    "location": {"type": "Point", "coordinates": [-73.97, 40.77]},
    "importance_score": 0.6,
    # ... other fields
}

# Query memories near a location
pipeline = [
    {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [-73.98, 40.76]},
            "distanceField": "distance",
            "maxDistance": 1000,  # meters
            "spherical": True
        }
    }
]
```

## Security Considerations

### Connection Security

1. **Use SSL/TLS**: Always enable SSL for production:
   ```python
   connection_string = "mongodb://username:password@host:27017/memori?ssl=true"
   ```

2. **Authentication**: Use strong credentials:
   ```python
   # MongoDB Atlas automatically uses SSL
   connection_string = "mongodb+srv://user:strongpassword@cluster.mongodb.net/memori"
   ```

3. **Network Security**: 
   - Whitelist IP addresses in Atlas
   - Use VPN for private networks
   - Configure firewall rules

### Data Security

1. **Field-level encryption**: MongoDB supports client-side field-level encryption
2. **Role-based access**: Configure database users with minimal required permissions
3. **Audit logging**: Enable audit logs for compliance

### Input Validation

The MongoDB adapter includes built-in input validation:

```python
from memori.utils.input_validator import DatabaseInputValidator

# All search parameters are validated
validated = DatabaseInputValidator.validate_search_params(
    query, namespace, category_filter, limit
)
```

## Performance Optimization

### Best Practices

1. **Index Optimization**:
   - Monitor index usage with `db.collection.getIndexes()`
   - Remove unused indexes
   - Use compound indexes for multi-field queries

2. **Query Optimization**:
   - Use projection to limit returned fields
   - Limit result sets appropriately
   - Use aggregation pipeline for complex operations

3. **Connection Pooling**:
   ```python
   connector = MongoDBConnector({
       "connection_string": "mongodb://localhost:27017/memori",
       "maxPoolSize": 50,
       "serverSelectionTimeoutMS": 5000
   })
   ```

4. **Memory Management**:
   - Implement TTL indexes for automatic cleanup
   - Regular cleanup of expired memories
   - Monitor memory usage

### Performance Monitoring

```python
# Get database statistics
db_info = connector.get_database_info()
print(f"Collections: {db_info['collections_count']}")
print(f"Data size: {db_info['data_size']} bytes")

# Get memory statistics
stats = adapter.get_memory_stats(namespace="user_session")
print(f"Short-term memories: {stats['short_term_count']}")
print(f"Long-term memories: {stats['long_term_count']}")
```

## Migration from Other Databases

### From SQLite

```python
# Example migration script structure
def migrate_sqlite_to_mongodb():
    # 1. Connect to both databases
    sqlite_conn = SQLiteConnector("sqlite:///memori.db")
    mongo_conn = MongoDBConnector("mongodb://localhost:27017/memori")
    
    # 2. Extract data from SQLite
    sqlite_data = sqlite_conn.execute_query("SELECT * FROM short_term_memory")
    
    # 3. Transform data format
    mongo_documents = []
    for row in sqlite_data:
        doc = {
            "memory_id": row["memory_id"],
            "processed_data": json.loads(row["processed_data"]),
            "importance_score": float(row["importance_score"]),
            # ... transform other fields
        }
        mongo_documents.append(doc)
    
    # 4. Load into MongoDB
    mongo_adapter = MongoDBAdapter(mongo_conn)
    mongo_adapter.batch_store_memories(mongo_documents, "short_term")
```

### Data Transformation Notes

- JSON fields in SQL become native objects in MongoDB
- Foreign key relationships become document references or embedded documents
- SQL joins become MongoDB aggregation pipelines or embedded documents
- Consider denormalizing data for MongoDB's document model

## Troubleshooting

### Common Issues

1. **Connection Failures**:
   ```
   Error: Failed to connect to MongoDB
   ```
   - Check MongoDB server is running
   - Verify connection string format
   - Check network connectivity and firewall rules

2. **Authentication Errors**:
   ```
   Error: Authentication failed
   ```
   - Verify username and password
   - Check user permissions on database
   - For Atlas: verify user exists and has correct roles

3. **Index Creation Failures**:
   ```
   Error: Failed to create search indexes
   ```
   - Check database permissions
   - Verify collection exists
   - For text indexes: ensure MongoDB version supports text search

4. **Vector Search Not Available**:
   ```
   Warning: Vector search not available
   ```
   - Vector search requires MongoDB Atlas
   - Ensure vector search index is created
   - Check Atlas subscription tier

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.getLogger("pymongo").setLevel(logging.DEBUG)

settings = MemoriSettings()
settings.debug = True
settings.logging.level = "DEBUG"
```

### Performance Issues

1. **Slow Queries**:
   - Enable MongoDB profiler: `db.setProfilingLevel(2)`
   - Check index usage with `explain()`
   - Monitor with MongoDB Compass

2. **Memory Usage**:
   - Check working set size
   - Monitor connection pool usage
   - Implement proper cleanup procedures

## Example Applications

### Simple Chatbot Memory

```python
class ChatbotMemory:
    def __init__(self, mongo_connection_string):
        self.connector = MongoDBConnector(mongo_connection_string)
        self.adapter = MongoDBAdapter(self.connector)
        self.search = MongoDBSearchAdapter(self.connector)
    
    def remember(self, user_id, content, importance=0.5):
        memory = {
            "processed_data": {"content": content},
            "importance_score": importance,
            "category_primary": "conversation",
            "namespace": f"user_{user_id}",
            "searchable_content": content,
            "summary": content[:100]
        }
        return self.adapter.store_short_term_memory(memory)
    
    def recall(self, user_id, query, limit=5):
        return self.search.execute_fulltext_search(
            query=query,
            namespace=f"user_{user_id}",
            limit=limit
        )
```

### Personal Assistant

```python
class PersonalAssistant:
    def __init__(self, mongo_connection_string):
        self.connector = MongoDBConnector(mongo_connection_string)
        self.adapter = MongoDBAdapter(self.connector)
        self.search = MongoDBSearchAdapter(self.connector)
    
    def store_preference(self, user_id, preference):
        memory = {
            "processed_data": preference,
            "importance_score": 0.8,
            "category_primary": "user_preference",
            "namespace": f"user_{user_id}",
            "is_preference": True,
            "searchable_content": f"{preference['key']} {preference['value']}",
            "summary": f"User prefers {preference['key']}: {preference['value']}"
        }
        return self.adapter.store_long_term_memory(memory)
    
    def get_context(self, user_id, current_topic):
        # Get relevant memories for context
        memories = self.search.execute_fulltext_search(
            query=current_topic,
            namespace=f"user_{user_id}",
            limit=3
        )
        
        # Get user preferences
        preferences = self.adapter.get_long_term_memories(
            namespace=f"user_{user_id}",
            category_filter=["user_preference"],
            limit=5
        )
        
        return {"memories": memories, "preferences": preferences}
```

## Conclusion

MongoDB provides a powerful and flexible backend for Memori's memory storage system. Its document-based model, rich query capabilities, and vector search support (in Atlas) make it an excellent choice for AI applications requiring sophisticated memory management.

Key benefits:
- ✅ Flexible schema for diverse memory types
- ✅ Powerful text search and aggregation
- ✅ Vector similarity search (Atlas)
- ✅ Horizontal scaling capabilities  
- ✅ Rich ecosystem and tooling
- ✅ Strong consistency and ACID transactions

For production deployments, MongoDB Atlas is recommended for its managed service benefits, including automatic backups, monitoring, and vector search capabilities.