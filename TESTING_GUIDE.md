# Testing Guide for Memori SDK

This guide explains testing strategy, pytest basics, and recommendations for the Memori SDK project.

## Current Testing Situation

**Current State**: The project has test files in the `/tests` directory, but they are not proper pytest tests. The CI/CD pipeline is currently disabled for testing to prevent build failures.

**Test Files Found**:
- `/tests/` directory exists with various test files
- Files contain test functions but may not follow pytest conventions
- Test files cover: MySQL, PostgreSQL, LiteLLM, OpenAI integrations

## What is Pytest?

Pytest is Python's most popular testing framework. It makes it easy to write simple unit tests and complex functional tests.

### Key Concepts:

1. **Test Discovery**: Pytest automatically finds test files named `test_*.py` or `*_test.py`
2. **Test Functions**: Functions starting with `test_` are automatically run as tests
3. **Assertions**: Use simple `assert` statements to check if code works correctly
4. **Fixtures**: Reusable setup code for tests
5. **Coverage**: Measures how much of your code is tested

### Simple Example:

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

Run with: `pytest test_example.py`

## Why Testing Matters for Memori SDK

### 1. **Reliability**
- Ensures memory operations work correctly
- Prevents data loss or corruption
- Validates AI agent interactions

### 2. **Confidence in Releases**
- Safe to deploy new versions
- Catch bugs before users do
- Maintain backwards compatibility

### 3. **Documentation**
- Tests show how the code should be used
- Examples of expected behavior
- Living documentation that stays up-to-date

### 4. **Refactoring Safety**
- Change code without fear of breaking things
- Ensures optimizations don't break functionality
- Supports long-term maintainability

## Recommended Testing Strategy

### Phase 1: Basic Unit Tests (Start Here)
Focus on core functionality first:

```python
# test_memory_core.py
import pytest
from memori import MemoryClient

def test_memory_client_initialization():
    """Test that MemoryClient can be created successfully."""
    client = MemoryClient(connection_string="sqlite:///test.db")
    assert client is not None
    assert client.connection_string == "sqlite:///test.db"

def test_store_memory():
    """Test storing a memory."""
    client = MemoryClient(connection_string="sqlite:///test.db")
    result = client.store("user123", "I like pizza")
    assert result is not None
    assert "memory_id" in result

def test_retrieve_memory():
    """Test retrieving memories."""
    client = MemoryClient(connection_string="sqlite:///test.db")
    # Store a memory first
    client.store("user123", "I like pizza")
    
    # Retrieve memories
    memories = client.retrieve("user123", "food preferences")
    assert len(memories) > 0
    assert "pizza" in memories[0].content.lower()
```

### Phase 2: Integration Tests
Test how components work together:

```python
# test_integrations.py
def test_openai_integration():
    """Test OpenAI integration with memory."""
    # Test that OpenAI calls can store and retrieve context
    pass

def test_database_integration():
    """Test database operations."""
    # Test PostgreSQL/MySQL connectivity and operations
    pass
```

### Phase 3: End-to-End Tests
Test complete workflows:

```python
# test_workflows.py
def test_complete_agent_workflow():
    """Test full agent conversation with memory persistence."""
    # Simulate complete AI agent interaction
    pass
```

## Current Test Files Analysis

Your current `/tests` directory contains:
- Database comparison tests
- Integration tests for LiteLLM, MySQL, PostgreSQL
- OpenAI integration tests
- Utility functions

**Issues with Current Tests**:
1. Not following pytest naming conventions consistently
2. May have external dependencies (databases, API keys)
3. Some are performance tests rather than unit tests
4. Missing basic unit tests for core functionality

## Immediate Recommendations

### 1. **Start Simple** (Week 1-2)
```bash
# Create a new test file
touch tests/test_memori_core.py
```

Write 3-5 basic tests for core functions:
- Client initialization
- Memory storage
- Memory retrieval
- Basic error handling

### 2. **Set Up Test Environment** (Week 3)
```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-asyncio

# Create pytest configuration
echo "[tool.pytest.ini_options]
testpaths = ['tests']
python_files = ['test_*.py']
python_functions = ['test_*']
addopts = [
    '--strict-markers',
    '--disable-warnings',
    '-v'
]
" >> pyproject.toml
```

### 3. **Create Test Database** (Week 4)
Use SQLite for testing (no external dependencies):
```python
# conftest.py - pytest configuration
import pytest
import tempfile
import os
from memori import MemoryClient

@pytest.fixture
def test_db():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    yield f"sqlite:///{db_path}"
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def memory_client(test_db):
    """Create a test memory client."""
    return MemoryClient(connection_string=test_db)
```

### 4. **Gradually Enable CI** (Week 5)
Once you have basic tests working locally:
```yaml
# In ci.yml - replace the disabled test section with:
- name: Run tests
  run: |
    pytest tests/test_memori_core.py -v
```

## Learning Resources

### 1. **Pytest Documentation**
- Official docs: https://docs.pytest.org/
- Tutorial: https://docs.pytest.org/en/stable/getting-started.html

### 2. **Testing Best Practices**
- Write tests first (Test-Driven Development)
- One assertion per test when possible
- Use descriptive test names
- Test edge cases and error conditions

### 3. **Python Testing Books**
- "Test-Driven Development with Python" by Harry Percival
- "Effective Python Testing with Pytest" by Brian Okken

## File Structure Recommendation

```
memori/
├── memori/              # Source code
├── tests/               # Test files
│   ├── conftest.py      # Pytest configuration & fixtures
│   ├── test_core.py     # Core functionality tests
│   ├── test_database.py # Database operation tests
│   ├── test_integrations/ # Integration tests
│   │   ├── test_openai.py
│   │   ├── test_litellm.py
│   │   └── test_databases.py
│   └── test_examples/   # Example usage tests
├── pyproject.toml       # Pytest configuration
└── TESTING_GUIDE.md     # This file
```

## My Recommendation

**For your current situation, I recommend:**

1. **Don't worry about complex testing yet** - Focus on learning pytest basics with simple examples
2. **Start with 1-2 basic tests** - Test core memory storage/retrieval functions
3. **Use SQLite for testing** - Avoid complex database setup initially
4. **Keep CI disabled for tests** until you have working tests locally
5. **Learn gradually** - Add one new test per week as you learn

**Timeline**:
- **Month 1**: Learn pytest basics, write 5-10 simple tests
- **Month 2**: Add database tests with SQLite
- **Month 3**: Add integration tests for OpenAI/LiteLLM
- **Month 4**: Enable testing in CI/CD pipeline

Testing is important for professional software, but it's okay to learn it gradually while building your product. The key is to start simple and build up your testing skills over time.

## Quick Start Commands

```bash
# Install testing tools
pip install pytest pytest-cov

# Run tests (when you have some)
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest tests/test_core.py       # Run specific test file
pytest -k "test_storage"        # Run tests matching pattern
pytest --cov=memori             # Run with coverage report
```

Start with one simple test, get it working, then gradually add more. Testing is a skill that improves with practice!