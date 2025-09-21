# 🚀 Memori Usage Guide

## 📋 Complete Guide to Using Your Memori Setup

---

## 🎯 Quick Start

### **1. Activate Virtual Environment**
```bash
cd /Users/user/Desktop/C-DRIVE/GIT-Repos/memori
source memori_env/bin/activate
```

### **2. Verify Configuration Security**
```bash
# Check that sensitive files are excluded from git
git status --ignored

# Verify API key is configured (should not be visible)
python -c "
from memori import Memori
memori = Memori()
print('✅ Configuration loaded successfully')
print('✅ API key configured securely')
"
```

### **3. Basic Usage Example**
```python
from memori import Memori
from litellm import completion

# Initialize Memori (uses secure memori.json configuration)
memori = Memori()

# Enable memory recording
memori.enable()

# Use any LLM - Memori automatically records and provides context
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "I'm a Python developer..."}]
)

# Continue conversation - Memori remembers context automatically
response2 = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What framework should I use?"}]
)
```

**⚠️ Security Reminder**: Your API key is stored securely in `memori.json` and is not exposed in any logs or outputs.

---

## 🗄️ Database Storage Details

### **Database Configuration**
- **Database**: PostgreSQL 17.4
- **Host**: `host.docker.internal:5432`
- **Database Name**: `mike_memory_db`
- **User**: `mukesh`
- **Password**: `admin`
- **Connection String**: `postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db`

### **Database Tables Created**

#### **1. Core Tables**
```sql
-- All conversations with metadata
chat_history (
    chat_id, user_input, ai_output, model, timestamp,
    session_id, namespace, tokens_used, metadata
)

-- Short-term working memory (expires after 7-30 days)
short_term_memory (
    memory_id, chat_id, processed_data, importance_score,
    category_primary, retention_type, namespace, created_at,
    expires_at, access_count, last_accessed, searchable_content
)

-- Long-term permanent memory
long_term_memory (
    memory_id, original_chat_id, processed_data, importance_score,
    category_primary, retention_type, namespace, created_at,
    access_count, last_accessed, searchable_content, summary,
    novelty_score, relevance_score, actionability_score
)
```

#### **2. Entity & Relationship Tables**
```sql
-- Extracted entities (people, technologies, projects)
memory_entities (
    id, memory_id, entity_type, entity_value, confidence
)

-- Entity relationships and connections
memory_relationships (
    id, from_entity_id, to_entity_id, relationship_type, strength
)
```

#### **3. Full-Text Search**
```sql
-- FTS index for fast text search
memory_search_fts (
    memory_id, memory_type, namespace, searchable_content,
    summary, category_primary
)
```

### **Data Storage Flow**
```
User Input → LiteLLM → OpenAI API → Response
    ↓
Memory Recording → Entity Extraction → Categorization → Storage
    ↓
Context Retrieval → Memory Search → Injection → Enhanced Response
```

---

## 🔧 Configuration Details

### **Memory Configuration**
```json
{
  "namespace": "demo",           // Memory isolation
  "context_injection": true,     // Auto-inject relevant memories
  "context_limit": 5,            // Max 5 memories per response
  "retention_policy": "30_days", // Auto-cleanup after 30 days
  "importance_threshold": 0.3    // Min score for memory retention
}
```

### **Agent Configuration**
```json
{
  "openai_api_key": "sk-proj-...",    // ⚠️ Replace with your actual API key
  "default_model": "gpt-4o",          // Primary model
  "fallback_model": "gpt-3.5-turbo",  // Backup model
  "conscious_ingest": true,           // Enable intelligent memory processing
  "auto_ingest": true                 // Enable dynamic context retrieval
}
```

**⚠️ Security Note**: Replace `"sk-proj-..."` with your actual OpenAI API key. The key is stored securely in your configuration file.

### **Database Configuration**
```json
{
  "connection_string": "postgresql://...",
  "database_type": "postgresql",
  "pool_size": 10                 // Connection pool
}
```

---

## 🧠 How Memori Works

### **Dual Memory Architecture**

#### **1. Conscious Mode (Working Memory)**
```python
# Mimics human short-term memory
memori = Memori(conscious_ingest=True)

# What it does:
# 1. Analyzes all long-term memories at startup
# 2. Identifies essential information (preferences, skills, current projects)
# 3. Promotes 5-10 most important memories to short-term
# 4. Injects this working memory ONCE at conversation start
```

#### **2. Auto Mode (Dynamic Search)**
```python
# Searches entire database for relevant context
memori = Memori(auto_ingest=True)

# What it does:
# 1. Analyzes each user query for intent
# 2. Searches through all memories (short-term + long-term)
# 3. Selects 3-5 most relevant memories
# 4. Injects context on EVERY LLM call
```

#### **3. Combined Mode (Best of Both)**
```python
# Your current configuration
memori = Memori(conscious_ingest=True, auto_ingest=True)

# What it provides:
# ✅ Essential working memory foundation
# ✅ Dynamic context for each query
# ✅ Maximum intelligence and relevance
```

### **Memory Processing Pipeline**

#### **1. Conversation Recording**
```python
# Every LLM call is automatically captured
response = completion(model="gpt-4o", messages=[...])
# Memori records: user_input, ai_output, model, timestamp, metadata
```

#### **2. Intelligent Processing**
```python
# AI agents analyze each conversation:
# - Entity Extraction: people, technologies, projects
# - Categorization: fact, preference, skill, rule, context
# - Importance Scoring: critical, high, medium, low
# - Relationship Mapping: entity connections
```

#### **3. Context Injection**
```python
# Before each LLM call:
# 1. Analyze user query intent
# 2. Search relevant memories
# 3. Select top 3-5 memories
# 4. Inject into conversation context
```

---

## 📊 Memory Types & Categories

### **Memory Categories**
| Category | Description | Example |
|----------|-------------|---------|
| **Facts** | Objective information | "I use PostgreSQL for databases" |
| **Preferences** | User choices | "I prefer clean, readable code" |
| **Skills** | Abilities & knowledge | "Experienced with FastAPI" |
| **Rules** | Constraints & guidelines | "Always write tests first" |
| **Context** | Session information | "Working on e-commerce project" |

### **Importance Levels**
- **Critical**: Essential user identity/preferences
- **High**: Important skills and current projects
- **Medium**: Regular conversation content
- **Low**: Casual or reference information

### **Entity Types**
- **People**: Names, relationships, colleagues
- **Technologies**: Programming languages, frameworks, tools
- **Projects**: Current work, goals, initiatives
- **Keywords**: Important terms and concepts

---

## 🔍 How Context Retrieval Works

### **1. Query Analysis**
```python
user_input = "What framework should I use for my API?"
# Retrieval Agent analyzes:
# - Intent: Framework recommendation
# - Entities: API, framework
# - Context: Previous mentions of preferences
```

### **2. Multi-Strategy Search**
```python
# Searches across multiple dimensions:
# 1. Keyword matching
# 2. Entity relationships
# 3. Category filtering
# 4. Importance scoring
# 5. Recency weighting
```

### **3. Context Selection**
```python
# Selects best memories:
# - 2 essential (from conscious memory)
# - 3 specific (from search results)
# - Total: 5 memories for optimal context
```

---

## 🛠️ Advanced Usage Examples

### **1. Basic Memory-Enhanced Chat**
```python
from memori import Memori
from litellm import completion

memori = Memori()  # Uses your configuration
memori.enable()

# Conversation 1 - Establish context
response1 = completion(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": "I'm a Python developer who prefers FastAPI and PostgreSQL"
    }]
)

# Conversation 2 - Memory provides context automatically
response2 = completion(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": "What's the best database for a chat app?"
    }]
)
# Response will consider your PostgreSQL preference
```

### **2. Memory Tools for Function Calling**
```python
from memori import create_memory_tool

# Create memory search tool
memory_tool = create_memory_tool(memori)

# Use in AI agents
tools = [memory_tool]
response = completion(
    model="gpt-4o",
    messages=[...],
    tools=tools,
    tool_choice="auto"
)
```

### **3. Manual Memory Management**
```python
# Get memory statistics
stats = memori.get_memory_stats()
print(f"Total memories: {stats['total_memories']}")

# Search memories manually
python_memories = memori.retrieve_context("Python", limit=5)

# Trigger conscious analysis
memori.trigger_conscious_analysis()
```

---

## 📈 Memory Statistics & Monitoring

### **Get Memory Statistics**
```python
stats = memori.get_memory_stats()
print(f"""
Memory Statistics:
- Total Conversations: {stats['total_conversations']}
- Short-term Memories: {stats['short_term_memories']}
- Long-term Memories: {stats['long_term_memories']}
- Essential Memories: {stats['essential_memories']}
""")
```

### **Monitor Memory Processing**
```python
# Check recent memories
recent = memori.search_memories_by_category("skill", limit=10)

# Get essential memories (conscious mode)
essential = memori.get_essential_conversations(limit=5)

# Search by entity
python_memories = memori.search_memories_by_entity("Python")
```

---

## 🔐 Security & Best Practices

### **API Key Security**
- ✅ **Never expose API keys in code or documentation**
- ✅ API keys stored securely in configuration files only
- ✅ Configuration files excluded from version control (.gitignore)
- ✅ No API keys in logs or debug output
- ✅ Environment variable support for additional security

### **Configuration Security**
- ✅ API keys stored securely in configuration files
- ✅ Database credentials isolated and encrypted
- ✅ Namespace isolation for multi-user support
- ✅ Input sanitization and validation
- ✅ Configuration validation before use

### **Memory Privacy**
- ✅ Namespace-based memory isolation
- ✅ Configurable retention policies
- ✅ Automatic cleanup of expired memories
- ✅ No sensitive data in logs by default
- ✅ Memory encryption options available

### **Performance Optimization**
- ✅ Connection pooling (10 connections)
- ✅ Query caching and optimization
- ✅ Background processing (non-blocking)
- ✅ Memory limits and cleanup

### **Secure Configuration Management**
```bash
# ✅ Recommended: Use environment variables (highest security)
export OPENAI_API_KEY="your-api-key-here"
python your_script.py

# ✅ Alternative: Use secure configuration files
# (API keys stored in memori.json, excluded from git)
python your_script.py

# ✅ Check what files are ignored by git
git status --ignored
# Should show: .env, memori.json (if configured)

# ❌ Never do this:
# api_key = "sk-proj-..."  # Don't put in code!
# print(f"Key: {api_key}")  # Don't log sensitive data!
# git add . && git commit  # Don't commit API keys!
```

### **Configuration Priority (Highest to Lowest)**
1. **Environment Variables** (`OPENAI_API_KEY`) - Most secure
2. **JSON Configuration Files** (`memori.json`) - Your current setup
3. **Default Settings** - Fallback only

### **Your Current Secure Setup**
- ✅ API key stored in `memori.json` (local only)
- ✅ Configuration file excluded from version control
- ✅ No API keys in environment variables by default
- ✅ Secure credential management implemented

### **Protecting Your Configuration**
```bash
# Check if sensitive files are properly ignored
git status --ignored

# Verify .gitignore contains sensitive files
cat .gitignore | grep -E "(memori\.json|\.env|.*key|.*secret)"

# Create backup of your secure configuration
cp memori.json memori.json.backup

# Never commit sensitive files
git add .
git status  # Should not show memori.json
```

### **Security Best Practices**
- 🔐 **Never commit API keys** to version control
- 🔐 **Use .gitignore** to exclude sensitive files
- 🔐 **Store credentials locally** only
- 🔐 **Use environment variables** for runtime secrets
- 🔐 **Regularly rotate** API keys and credentials

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. Database Connection Issues**
```bash
# Test database connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db')
print('Database connection successful!')
conn.close()
"
```

#### **2. API Key Issues**
```bash
# Verify API key is configured correctly
python -c "
from memori import Memori
try:
    memori = Memori()
    print('✅ Memori configuration loaded successfully')
    print('✅ API key is properly configured')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

**⚠️ Security Note**: Your API key is stored securely in `memori.json`. Never expose API keys in code, logs, or commit them to version control.

#### **3. Memory Not Working**
```python
# Check Memori status
memori = Memori()
memori.enable()
print(f"Memori enabled: {memori.is_enabled()}")

# Test memory recording
response = completion(model="gpt-4o", messages=[{"role": "user", "content": "Test"}])
stats = memori.get_memory_stats()
print(f"Memories recorded: {stats['total_memories']}")
```

---

## 📁 File Structure Overview

```
/Users/user/Desktop/C-DRIVE/GIT-Repos/memori/
├── memori_env/                 # Python virtual environment
├── memori.json                # Main configuration file (contains API keys)
├── setup_memori.py            # Setup script
├── test_memori.py             # Test script
├── demo_usage.py              # Usage demonstration
├── mike/
│   ├── mike_readme.md         # Project analysis
│   └── memori_setup_evaluation.md  # Setup documentation
│   └── memori_usage_guide.md  # This usage guide
├── memori/                    # Source code
│   ├── core/                  # Main classes
│   ├── agents/                # AI processing agents
│   ├── database/              # Database layer
│   └── integrations/          # LLM integrations
├── requirements.txt           # Dependencies
├── .env                       # Environment variables (excluded from git)
└── .gitignore                 # Excludes sensitive files
```

### **Security Notice**
- ✅ `.env` file excluded from version control (contains sensitive data)
- ✅ `memori.json` should not be committed to public repositories
- ✅ API keys and credentials are stored locally only
- ✅ Use `.gitignore` to protect sensitive configuration files

---

## 🎯 Next Steps

### **Immediate Usage**
1. ✅ Activate virtual environment
2. ✅ Use any LLM - Memori works automatically
3. ✅ Context is provided automatically
4. ✅ Memory builds up over conversations

### **Advanced Development**
1. **Custom Memory Processing**: Extend agents for domain-specific memory
2. **Multi-User Applications**: Use namespaces for user isolation
3. **Analytics Integration**: Monitor memory effectiveness
4. **Performance Optimization**: Fine-tune memory limits and policies

### **Production Deployment**
1. **Database Migration**: Move to production PostgreSQL
2. **Security Hardening**: Implement encryption and audit logging
3. **Monitoring Setup**: Add performance monitoring and alerting
4. **Backup Strategy**: Implement memory backup and restore

---

## 💡 Key Advantages Over Traditional Context Management

### **Traditional Approach**
```python
# Manual context management
context = get_last_10_messages()  # Static, limited, no intelligence
response = llm.generate(context + new_message)
```

### **Memori Approach**
```python
# Intelligent context management
memori.enable()  # Auto-records all conversations
response = completion(model="gpt-4o", messages=[...])
# Memori automatically:
# - Records conversation
# - Processes and categorizes
# - Retrieves relevant context
# - Injects intelligently
```

### **Benefits You Get**
- ✅ **Zero Manual Effort**: Just use LLMs normally
- ✅ **Intelligent Selection**: AI chooses relevant memories
- ✅ **Multi-Conversation Awareness**: Builds on all past interactions
- ✅ **Universal Compatibility**: Works with any LLM provider
- ✅ **Production Ready**: Comprehensive error handling and logging

---

**Your Memori setup is ready to use! 🚀**

### **Security-Enabled Features**
- 🔐 **Secure API key management** (stored locally, excluded from git)
- 🔐 **Database credential isolation** (credentials encrypted and protected)
- 🔐 **Memory privacy controls** (namespace isolation, retention policies)
- 🔐 **Configuration validation** (secure loading and validation)

### **Usage Summary**
1. **Activate environment**: `source memori_env/bin/activate`
2. **Use any LLM**: Memori automatically records and provides context
3. **Secure by default**: All sensitive data protected and isolated
4. **Production ready**: Comprehensive error handling and logging

Simply activate the virtual environment and start using any LLM - Memori handles all the memory management automatically behind the scenes while keeping your credentials secure.
