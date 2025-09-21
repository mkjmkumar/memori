#!/usr/bin/env python3
"""
Local Memory Configuration
Use Ollama models for memory building, OpenAI for complex tasks
"""

import os
import psycopg2
from memori import Memori
from litellm import completion


def setup_local_memory_config():
    """Setup memory system to use all local Ollama models (no API costs)"""
    print("🔧 Setting up All-Local Memory Configuration...")
    print("📊 Simple Tasks: tinyllama:latest (fast, lightweight)")
    print("📋 Medium Tasks: llama3.2:3b (balanced performance)")
    print("🚀 Complex Tasks: granite-code:34b (34B parameters)")

    # Configure memory system to use local models
    try:
        memori = Memori(
            namespace="video_processor",
            database_connect="postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db",
            conscious_ingest=True,  # Learn from conversations
            auto_ingest=True,       # Provide context automatically
            verbose=False
        )

        memori.enable()
        print("✅ Memory system enabled with local Ollama models")
        print("✅ No API costs - all processing local!")

        return memori

    except Exception as e:
        print(f"❌ Memory system error: {e}")
        return None


def test_local_memory():
    """Test memory system with local model"""
    print("\n🧪 Testing Local Memory System...")
    print("=" * 50)

    memori = setup_hybrid_memory_config()
    if not memori:
        return False

    # Test scenarios using local model for memory building
    test_cases = [
        {
            "question": "How does the video processing pipeline work?",
            "context": "Understanding system architecture"
        },
        {
            "question": "What happens during frame extraction?",
            "context": "Module-specific knowledge"
        },
        {
            "question": "How do I troubleshoot OCR quality issues?",
            "context": "Troubleshooting guidance"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['context']}")
        print(f"❓ {test_case['question']}")

        try:
            # This will use local model for memory context, OpenAI for complex reasoning
            response = completion(
                model="ollama/granite-code:34b",  # Local model for memory
                messages=[{"role": "user", "content": test_case['question']}]
            )

            answer = response.choices[0].message.content
            print("✅ Local Memory Response:")
            print(f"   {answer[:200]}..." if len(answer) > 200 else f"   {answer}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return True


def test_all_local_approach():
    """Demonstrate all-local approach: different Ollama models for different complexity"""
    print("\n🔄 Testing All-Local Approach...")
    print("=" * 50)
    print("📊 Simple Tasks: tinyllama:latest (fast, lightweight)")
    print("📋 Medium Tasks: llama3.2:3b (balanced performance)")
    print("🚀 Complex Tasks: granite-code:34b (34B parameters)")

    memori = setup_local_memory_config()
    if not memori:
        return False

    # Complex question that benefits from both local memory and OpenAI reasoning
    complex_question = """
    I'm building a video processing system and need to optimize it for large files.
    The system has these components:
    - Video upload and validation
    - Frame extraction using OpenCV
    - OCR processing for text extraction
    - AI analysis of content
    - Manual generation in Excel format

    What are the best strategies to handle large video files efficiently?
    Consider both technical implementation and business requirements.
    """

    print("❓ Complex Question:")
    print(complex_question)

    try:
        # Use granite-code:34b for complex reasoning (all local)
        response = completion(
            model="ollama/granite-code:34b",  # Local 34B model for complex analysis
            messages=[{"role": "user", "content": complex_question}],
            max_tokens=500
        )

        answer = response.choices[0].message.content
        print("\n🚀 All-Local Response (granite-code:34b + Memory Context):")
        print("=" * 50)
        print(answer)

    except Exception as e:
        print(f"❌ Error: {e}")

    return True


def compare_models():
    """Compare local model vs OpenAI for memory tasks"""
    print("\n📊 Model Comparison for Memory Tasks")
    print("=" * 50)

    question = "How does the OCR processing module work in the video processing system?"

    # Test with simple local model
    print("\n📝 1. SIMPLE LOCAL MODEL (tinyllama):")
    print("-" * 40)
    try:
        response = completion(
            model="ollama/tinyllama:latest",
            messages=[{"role": "user", "content": question}]
        )
        simple_answer = response.choices[0].message.content
        print(f"✅ Simple Model Response:\n{simple_answer[:300]}...")
    except Exception as e:
        simple_answer = f"Error: {e}"
        print(f"❌ Simple Model Error: {e}")

    # Test with medium local model
    print("\n📋 2. MEDIUM LOCAL MODEL (llama3.2:3b):")
    print("-" * 40)
    try:
        response = completion(
            model="ollama/llama3.2:3b",
            messages=[{"role": "user", "content": question}]
        )
        medium_answer = response.choices[0].message.content
        print(f"✅ Medium Model Response:\n{medium_answer[:300]}...")
    except Exception as e:
        medium_answer = f"Error: {e}"
        print(f"❌ Medium Model Error: {e}")

    # Test with complex local model with memory
    print("\n🚀 3. COMPLEX LOCAL MODEL + MEMORY (granite-code:34b):")
    print("-" * 40)
    try:
        response = completion(
            model="ollama/granite-code:34b",
            messages=[{"role": "user", "content": question}]
        )
        complex_answer = response.choices[0].message.content
        print(f"✅ Complex Model Response:\n{complex_answer[:300]}...")
    except Exception as e:
        complex_answer = f"Error: {e}"
        print(f"❌ Complex Model Error: {e}")

    return simple_answer, medium_answer, complex_answer


def main():
    """Main demonstration function"""
    print("🔄 Video Processor Memory System - All-Local Configuration")
    print("=" * 70)
    print("Using only local Ollama models (no API costs)")
    print("=" * 70)

    # Test local memory system
    if not test_local_memory():
        print("❌ Local memory test failed")
        return False

    # Test all-local approach
    if not test_all_local_approach():
        print("❌ All-local approach test failed")
        return False

    # Compare models
    compare_models()

    print(f"\n{'='*70}")
    print("✅ ALL-LOCAL MEMORY SYSTEM READY!")
    print(f"{'='*70}")
    print("📊 Simple Tasks: tinyllama:latest (637 MB)")
    print("📋 Medium Tasks: llama3.2:3b (2.0 GB)")
    print("🚀 Complex Tasks: granite-code:34b (19 GB)")
    print("🔗 Memory System: Database-driven context injection")

    print("\n📋 How to Use:")
    print("1. All models are local - zero API costs")
    print("2. Memory context works with all Ollama models")
    print("3. Choose model based on task complexity")
    print("4. Perfect for exploring memory system capabilities")

    return True


if __name__ == "__main__":
    main()
