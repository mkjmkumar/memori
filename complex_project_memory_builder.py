#!/usr/bin/env python3
"""
Complex Project Memory Builder
Automated system for building comprehensive memory across multiple modules
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from memori import Memori, create_memory_tool
from litellm import completion


@dataclass
class ModuleInfo:
    """Information about a project module"""
    name: str
    category: str  # core, services, integration, deployment, utilities
    priority: str  # critical, high, medium, low
    description: str
    files: List[str]
    dependencies: List[str]
    api_endpoints: List[str]
    configuration: Dict[str, Any]


@dataclass
class ProjectMemoryConfig:
    """Configuration for project memory building"""
    project_name: str
    modules: Dict[str, ModuleInfo]
    base_namespace: str
    memory_modes: Dict[str, bool]  # conscious_ingest, auto_ingest
    retention_policies: Dict[str, str]


class ComplexProjectMemoryBuilder:
    """Builds comprehensive memory for complex multi-module projects"""

    def __init__(self, config: ProjectMemoryConfig):
        self.config = config
        self.memori_instances = {}
        self._setup_memori_instances()

    def _setup_memori_instances(self):
        """Create Memori instances for different namespaces"""
        base_config = {
            "database_connect": "postgresql://mukesh:admin@host.docker.internal:5432/mike_memory_db",
            "verbose": True
        }

        # Main project memory
        self.memori_instances["main"] = Memori(
            namespace=self.config.base_namespace,
            conscious_ingest=self.config.memory_modes["conscious_ingest"],
            auto_ingest=self.config.memory_modes["auto_ingest"],
            **base_config
        )

        # Module-specific memories
        for module_name, module_info in self.config.modules.items():
            namespace = f"{self.config.base_namespace}.{module_info.category}.{module_name}"
            self.memori_instances[module_name] = Memori(
                namespace=namespace,
                conscious_ingest=module_info.priority in ["critical", "high"],
                auto_ingest=module_info.priority in ["medium", "low"],
                **base_config
            )

    def enable_all_memories(self):
        """Enable all memory instances"""
        for name, memori in self.memori_instances.items():
            memori.enable()
            print(f"✅ Enabled memory for: {name}")

    def ingest_module_documentation(self, module_name: str, doc_content: str):
        """Ingest documentation for a specific module"""
        if module_name not in self.memori_instances:
            print(f"❌ Module {module_name} not found in configuration")
            return False

        memori = self.memori_instances[module_name]

        try:
            # Create comprehensive documentation context
            doc_messages = [
                {
                    "role": "system",
                    "content": f"You are documenting the {module_name} module. Extract and organize all technical information, APIs, configuration details, and integration points."
                },
                {
                    "role": "user",
                    "content": f"Please analyze and document this {module_name} module:\n\n{doc_content}"
                }
            ]

            # Process documentation
            response = completion(
                model="gpt-4o",
                messages=doc_messages
            )

            print(f"✅ Ingested documentation for {module_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to ingest documentation for {module_name}: {e}")
            return False

    def analyze_codebase(self, module_name: str, code_files: List[str]):
        """Analyze codebase files for a module"""
        if module_name not in self.memori_instances:
            print(f"❌ Module {module_name} not found in configuration")
            return False

        memori = self.memori_instances[module_name]

        try:
            for file_path in code_files:
                if not Path(file_path).exists():
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()

                # Analyze code structure
                code_analysis = self._analyze_code_file(file_path, code_content)

                # Record in memory
                response = completion(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": f"Analyze this {module_name} code for memory building:\n\nFile: {file_path}\n\n{code_content}"
                    }]
                )

                print(f"✅ Analyzed code file: {file_path}")

            return True

        except Exception as e:
            print(f"❌ Failed to analyze codebase for {module_name}: {e}")
            return False

    def _analyze_code_file(self, file_path: str, code_content: str) -> Dict[str, Any]:
        """Analyze individual code file structure"""
        analysis = {
            "file_path": file_path,
            "file_type": Path(file_path).suffix,
            "functions": [],
            "classes": [],
            "imports": [],
            "dependencies": [],
            "api_endpoints": [],
            "configuration": {}
        }

        # Extract key information
        lines = code_content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('def '):
                analysis["functions"].append(line.split('(')[0].replace('def ', ''))
            elif line.startswith('class '):
                analysis["classes"].append(line.split('(')[0].replace('class ', ''))
            elif line.startswith('import ') or line.startswith('from '):
                analysis["imports"].append(line)

        return analysis

    def capture_expert_knowledge(self, module_name: str, expert_notes: str):
        """Capture expert insights and domain knowledge"""
        if module_name not in self.memori_instances:
            print(f"❌ Module {module_name} not found in configuration")
            return False

        memori = self.memori_instances[module_name]

        try:
            # Structure expert knowledge
            expert_messages = [
                {
                    "role": "system",
                    "content": "You are capturing expert knowledge about software modules. Extract technical insights, best practices, troubleshooting information, and architectural decisions."
                },
                {
                    "role": "user",
                    "content": f"Capture expert knowledge for {module_name}:\n\n{expert_notes}"
                }
            ]

            response = completion(
                model="gpt-4o",
                messages=expert_messages
            )

            print(f"✅ Captured expert knowledge for {module_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to capture expert knowledge for {module_name}: {e}")
            return False

    def build_cross_module_relationships(self):
        """Build relationships between modules"""
        print("🔗 Building cross-module relationships...")

        try:
            main_memori = self.memori_instances["main"]

            # Analyze relationships between modules
            for module_name, module_info in self.config.modules.items():
                relationship_content = f"""
                Module: {module_name}
                Category: {module_info.category}
                Dependencies: {', '.join(module_info.dependencies)}
                Description: {module_info.description}

                Relationships with other modules should be analyzed for:
                - Data flow connections
                - API integrations
                - Shared utilities
                - Configuration dependencies
                """

                response = completion(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": f"Analyze cross-module relationships:\n\n{relationship_content}"
                    }]
                )

            print("✅ Cross-module relationships established")
            return True

        except Exception as e:
            print(f"❌ Failed to build relationships: {e}")
            return False

    def generate_memory_report(self) -> Dict[str, Any]:
        """Generate comprehensive memory report"""
        report = {
            "project_name": self.config.project_name,
            "total_modules": len(self.config.modules),
            "memory_instances": len(self.memori_instances),
            "configuration": self.config.__dict__,
            "module_coverage": {},
            "memory_statistics": {}
        }

        # Gather statistics from all memory instances
        for name, memori in self.memori_instances.items():
            try:
                stats = memori.get_memory_stats()
                report["memory_statistics"][name] = stats

                # Test memory retrieval
                context = memori.retrieve_context("general overview", limit=3)
                report["module_coverage"][name] = len(context)

            except Exception as e:
                report["memory_statistics"][name] = f"Error: {e}"

        return report

    def get_memory_insights(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Get insights from project memory"""
        insights = {}

        # Query main project memory
        try:
            main_context = self.memori_instances["main"].retrieve_context(query, limit=limit)
            insights["main"] = main_context
        except Exception as e:
            insights["main"] = f"Error: {e}"

        # Query module-specific memories
        for module_name in self.config.modules.keys():
            try:
                module_context = self.memori_instances[module_name].retrieve_context(query, limit=limit//2)
                insights[module_name] = module_context
            except Exception as e:
                insights[module_name] = f"Error: {e}"

        return insights


def create_sample_project_config() -> ProjectMemoryConfig:
    """Create a sample configuration for a complex project"""

    modules = {
        # Core Pipeline Modules
        "data_ingestion": ModuleInfo(
            name="data_ingestion",
            category="core",
            priority="critical",
            description="Handles incoming data from various sources",
            files=["src/data_ingestion/*.py"],
            dependencies=["database_connector", "data_validator"],
            api_endpoints=["/api/v1/data/upload", "/api/v1/data/validate"],
            configuration={"batch_size": 1000, "timeout": 30}
        ),

        "data_processing": ModuleInfo(
            name="data_processing",
            category="core",
            priority="critical",
            description="Processes and transforms raw data",
            files=["src/data_processing/*.py"],
            dependencies=["data_ingestion", "model_training"],
            api_endpoints=["/api/v1/process/batch", "/api/v1/process/stream"],
            configuration={"parallel_workers": 4, "cache_enabled": True}
        ),

        # Service Modules
        "user_management": ModuleInfo(
            name="user_management",
            category="services",
            priority="high",
            description="Manages user accounts and authentication",
            files=["src/services/user_service.py"],
            dependencies=["database_connector", "authentication"],
            api_endpoints=["/api/v1/users", "/api/v1/auth/login"],
            configuration={"session_timeout": 3600, "max_login_attempts": 3}
        ),

        "notification_service": ModuleInfo(
            name="notification_service",
            category="services",
            priority="medium",
            description="Handles user notifications and alerts",
            files=["src/services/notification_service.py"],
            dependencies=["user_management", "message_queue"],
            api_endpoints=["/api/v1/notifications/send", "/api/v1/notifications/bulk"],
            configuration={"email_provider": "sendgrid", "sms_provider": "twilio"}
        ),

        # Integration Modules
        "api_gateway": ModuleInfo(
            name="api_gateway",
            category="integration",
            priority="high",
            description="Main API entry point and routing",
            files=["src/integration/api_gateway.py"],
            dependencies=["user_management", "data_processing"],
            api_endpoints=["/api/v1/*"],
            configuration={"rate_limiting": True, "cors_enabled": True}
        )
    }

    return ProjectMemoryConfig(
        project_name="MyComplexProject",
        modules=modules,
        base_namespace="my_complex_project",
        memory_modes={
            "conscious_ingest": True,  # Essential information always available
            "auto_ingest": True       # Dynamic context retrieval
        },
        retention_policies={
            "critical": "permanent",
            "high": "2_years",
            "medium": "1_year",
            "low": "6_months"
        }
    )


async def main():
    """Main function for memory building"""
    print("🏗️ Complex Project Memory Builder")
    print("=" * 50)

    # Create project configuration
    config = create_sample_project_config()

    print(f"📋 Project: {config.project_name}")
    print(f"📊 Total Modules: {len(config.modules)}")
    print(f"🏗️ Memory Architecture: {config.base_namespace}")
    print()

    # Initialize memory builder
    builder = ComplexProjectMemoryBuilder(config)
    builder.enable_all_memories()

    print("\n" + "=" * 50)
    print("🎯 MEMORY BUILDING PHASES")
    print("=" * 50)

    # Phase 1: Documentation Ingestion
    print("\n📚 Phase 1: Documentation Ingestion")
    for module_name, module_info in config.modules.items():
        print(f"  • Ingesting docs for: {module_name}")
        # In real implementation, read from actual documentation files
        sample_doc = f"This is the {module_name} module documentation. It handles {module_info.description}."
        builder.ingest_module_documentation(module_name, sample_doc)

    # Phase 2: Code Analysis
    print("\n💻 Phase 2: Code Analysis")
    for module_name, module_info in config.modules.items():
        print(f"  • Analyzing code for: {module_name}")
        # In real implementation, analyze actual source files
        sample_files = [f"src/{module_name}/main.py", f"src/{module_name}/utils.py"]
        builder.analyze_codebase(module_name, sample_files)

    # Phase 3: Expert Knowledge
    print("\n🧠 Phase 3: Expert Knowledge Capture")
    for module_name, module_info in config.modules.items():
        print(f"  • Capturing expert insights for: {module_name}")
        expert_notes = f"Expert notes for {module_name}: Best practices and implementation details."
        builder.capture_expert_knowledge(module_name, expert_notes)

    # Phase 4: Cross-module relationships
    print("\n🔗 Phase 4: Cross-Module Relationships")
    builder.build_cross_module_relationships()

    # Generate final report
    print("\n📊 Generating Memory Report...")
    report = builder.generate_memory_report()

    print("\n" + "=" * 50)
    print("🎉 MEMORY BUILDING COMPLETE")
    print("=" * 50)

    print(f"📊 Total Memory Instances: {report['memory_instances']}")
    print(f"📈 Project Coverage: {len(report['module_coverage'])} modules")
    print(f"🗄️ Memory Statistics: {len(report['memory_statistics'])} namespaces")

    # Show sample insights
    print("\n🔍 Sample Memory Insights:")
    insights = builder.get_memory_insights("best practices", limit=2)

    for namespace, context in insights.items():
        if isinstance(context, list) and context:
            print(f"  • {namespace}: {len(context)} insights available")

    print("\n✅ Your complex project memory system is ready!")
    print("💡 Use builder.get_memory_insights() for project-wide queries")
    print("🔍 Use individual memori instances for module-specific queries")


if __name__ == "__main__":
    asyncio.run(main())
