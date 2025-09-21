#!/usr/bin/env python3
"""
Quick Start: Complex Project Memory Implementation
Step-by-step guide to get started with your 20-module project
"""

from complex_project_memory_builder import ComplexProjectMemoryBuilder, ProjectMemoryConfig, ModuleInfo
from memori import Memori
import json


def create_your_project_config():
    """Create configuration for your specific project"""

    # Replace with your actual project details
    your_modules = {
        # Add your 20 modules here following the template
        "your_module_1": ModuleInfo(
            name="your_module_1",
            category="core",  # core, services, integration, deployment, utilities
            priority="critical",  # critical, high, medium, low
            description="Description of your first module",
            files=["path/to/your/files.py"],
            dependencies=["other_module_name"],
            api_endpoints=["/api/v1/endpoint"],
            configuration={"key": "value"}
        ),
        # Add more modules...
    }

    config = ProjectMemoryConfig(
        project_name="YOUR_ACTUAL_PROJECT_NAME",
        modules=your_modules,
        base_namespace="your_project",  # Replace with your project name
        memory_modes={
            "conscious_ingest": True,  # Essential info always available
            "auto_ingest": True        # Dynamic context for queries
        },
        retention_policies={
            "critical": "permanent",
            "high": "2_years",
            "medium": "1_year",
            "low": "6_months"
        }
    )

    return config


def quick_start_demo():
    """Quick demonstration of the memory system"""

    print("🚀 Quick Start: Complex Project Memory")
    print("=" * 50)

    # 1. Create your project configuration
    print("1️⃣ Creating project configuration...")
    config = create_your_project_config()
    print(f"   ✅ Project: {config.project_name}")
    print(f"   ✅ Modules: {len(config.modules)}")
    print(f"   ✅ Base namespace: {config.base_namespace}")

    # 2. Initialize memory builder
    print("\n2️⃣ Initializing memory builder...")
    builder = ComplexProjectMemoryBuilder(config)
    builder.enable_all_memories()
    print("   ✅ Memory instances created and enabled")

    # 3. Test memory recording
    print("\n3️⃣ Testing memory recording...")

    # Create sample conversations for each module
    sample_conversations = {
        "data_ingestion": "How does the data ingestion module work? It handles CSV and JSON files from external APIs.",
        "user_management": "The user management service handles authentication and user profiles.",
        "api_gateway": "Our API gateway routes requests to appropriate services and handles rate limiting."
    }

    for module_name, conversation in sample_conversations.items():
        if module_name in builder.config.modules:
            print(f"   📝 Recording: {module_name}")

            # This would normally be actual LLM conversations
            # For demo, we'll simulate the memory recording
            print(f"   💾 Memory recorded for {module_name}")

    # 4. Test memory retrieval
    print("\n4️⃣ Testing memory retrieval...")

    # Query across modules
    test_queries = [
        "How does data flow through the system?",
        "What are the main API endpoints?",
        "How do modules communicate with each other?"
    ]

    for query in test_queries:
        print(f"   🔍 Query: {query}")
        insights = builder.get_memory_insights(query, limit=2)
        print(f"   📊 Found insights in {len(insights)} namespaces")

    # 5. Generate memory report
    print("\n5️⃣ Generating memory report...")
    report = builder.generate_memory_report()

    print("   📊 Report generated:")
    print(f"   • Project: {report['project_name']}")
    print(f"   • Total modules: {report['total_modules']}")
    print(f"   • Memory instances: {report['memory_instances']}")

    print("\n" + "=" * 50)
    print("🎉 Quick Start Complete!")
    print("=" * 50)

    print("\n📋 Next Steps:")
    print("1. Customize complex_project_config_template.json")
    print("2. Run the full memory builder: python complex_project_memory_builder.py")
    print("3. Start ingesting real documentation and code")
    print("4. Use the memory system in your development workflow")

    print("\n💡 Your memory system is ready to learn about your 20 modules!")


def setup_your_project():
    """Setup instructions for your project"""

    print("\n📋 SETUP INSTRUCTIONS FOR YOUR PROJECT")
    print("=" * 50)

    print("\n1️⃣ CONFIGURE YOUR PROJECT:")
    print("   • Edit: complex_project_config_template.json")
    print("   • Add your 20 module names and details")
    print("   • Update file paths to match your structure")

    print("\n2️⃣ CUSTOMIZE MODULE CATEGORIES:")
    print("   • core: Pipeline modules (critical path)")
    print("   • services: Business logic modules")
    print("   • integration: External connections")
    print("   • deployment: Infrastructure modules")
    print("   • utilities: Shared tools and helpers")

    print("\n3️⃣ SET PRIORITIES:")
    print("   • critical: Essential pipeline modules")
    print("   • high: Important service modules")
    print("   • medium: Standard modules")
    print("   • low: Utility/reference modules")

    print("\n4️⃣ GATHER CONTENT:")
    print("   • Documentation files (README, API docs)")
    print("   • Source code files")
    print("   • Expert knowledge and notes")
    print("   • Configuration files")

    print("\n5️⃣ START BUILDING MEMORY:")
    print("   python complex_project_memory_builder.py")

    print("\n✅ Pro Tips:")
    print("   • Start with 3-5 critical modules first")
    print("   • Use the demo to understand the flow")
    print("   • Customize the memory builder for your needs")
    print("   • Monitor memory growth and quality")
    print("   • Integrate with your development workflow")


if __name__ == "__main__":
    print("🚀 Complex Project Memory - Quick Start Guide")
    print("=" * 50)
    print("This guide helps you start building memory for your 20-module project!")
    print("=" * 50)

    # Run demo
    quick_start_demo()

    # Show setup instructions
    setup_your_project()

    print("\n" + "=" * 50)
    print("📚 FILES CREATED FOR YOUR PROJECT:")
    print("=" * 50)
    print("• complex_project_memory_builder.py  # Main memory builder")
    print("• complex_project_config_template.json # Configuration template")
    print("• complex_project_quick_start.py     # This quick start guide")
    print("• mike/complex_project_memory_strategy.md # Detailed strategy")

    print("\n💡 Next: Edit the config template with your 20 modules!")
    print("🔧 Then run: python complex_project_memory_builder.py")

