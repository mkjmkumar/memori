#!/usr/bin/env python3
"""
Setup Memory Configuration
Automatically loads configuration from database and sets environment variables
"""

import os
import psycopg2
from pathlib import Path


def load_config_from_database():
    """Load configuration from database and set environment variables"""
    try:
        # Database connection
        conn = psycopg2.connect('postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db')
        cur = conn.cursor()

        # Load all configuration from secure_config table
        cur.execute('SELECT key_name, key_value FROM secure_config')
        configs = cur.fetchall()

        print("📊 Loading configuration from database...")

        loaded_count = 0
        for key_name, key_value in configs:
            # Convert database key names to environment variable names
            env_key_map = {
                'openai_api_key': 'OPENAI_API_KEY',
                'openai_organization_id': 'OPENAI_ORGANIZATION_ID',
                'openai_project_id': 'OPENAI_PROJECT_ID',
                'openai_model': 'OPENAI_MODEL',
                'openai_api_base': 'OPENAI_API_BASE',
                'embedding_model': 'EMBEDDING_MODEL',
                'embedding_dimensions': 'EMBEDDING_DIMENSIONS',
                'embedding_rate_limit_retries': 'EMBEDDING_RATE_LIMIT_RETRIES',
                'embedding_api_timeout': 'EMBEDDING_API_TIMEOUT',
                'embedding_retry_delay': 'EMBEDDING_RETRY_DELAY'
            }

            if key_name in env_key_map:
                env_var = env_key_map[key_name]
                os.environ[env_var] = str(key_value)
                print(f"✅ {env_var}: Loaded from database")
                loaded_count += 1

        cur.close()
        conn.close()

        print(f"✅ Configuration loaded: {loaded_count} variables set")
        return True

    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False


def test_memory_system():
    """Test that the memory system works with loaded configuration"""
    print("\n🧠 Testing Memory System...")

    try:
        from memori import Memori

        memori = Memori(
            namespace="video_processor",
            database_connect="postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db",
            verbose=False
        )

        memori.enable()
        print("✅ Memory system: Enabled successfully")
        return True

    except Exception as e:
        print(f"❌ Memory system error: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Video Processor Memory System")
    print("=" * 50)

    # Load configuration from database
    if not load_config_from_database():
        print("❌ Failed to load configuration from database")
        return False

    # Test memory system
    if not test_memory_system():
        print("❌ Memory system test failed")
        return False

    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print("✅ Configuration loaded from database")
    print("✅ Environment variables set")
    print("✅ Memory system tested and working")
    print("✅ Ready to use!")

    print("\n📋 You can now run:")
    print("  python video_processor_memory_demo.py")
    print("  python test_memory_functionality.py")

    return True


if __name__ == "__main__":
    main()
