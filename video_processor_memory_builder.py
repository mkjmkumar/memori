#!/usr/bin/env python3
"""
Video Processor Memory Builder
Specialized memory system for the Operational Video Manual Generation project
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from memori import Memori, create_memory_tool
from litellm import completion


@dataclass
class VideoProcessorModule:
    """Video Processor specific module information"""
    name: str
    category: str
    priority: str
    description: str
    workflow_stage: int
    input_types: List[str]
    output_types: List[str]
    dependencies: List[str]
    technologies: List[str]
    common_issues: List[str]
    best_practices: List[str]


@dataclass
class VideoProcessorConfig:
    """Configuration for Video Processor memory building"""
    project_name: str
    modules: Dict[str, VideoProcessorModule]
    base_namespace: str
    processing_pipeline: List[str]
    memory_modes: Dict[str, bool]
    retention_policies: Dict[str, str]


class VideoProcessorMemoryBuilder:
    """Builds comprehensive memory for the Video Processor project"""

    def __init__(self, config: VideoProcessorConfig):
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
                conscious_ingest=module_info.priority == "critical",
                auto_ingest=module_info.priority in ["high", "medium"],
                **base_config
            )

    def enable_all_memories(self):
        """Enable all memory instances"""
        for name, memori in self.memori_instances.items():
            memori.enable()
            print(f"✅ Enabled memory for: {name}")

    def ingest_system_overview(self, overview_content: str):
        """Ingest the system overview into memory"""
        print("📚 Ingesting Video Processor system overview...")

        main_memori = self.memori_instances["main"]

        try:
            # Create comprehensive system overview memory
            system_prompt = f"""
            You are building memory for the Video Processor project - a system that creates operational user manuals from videos.

            System Overview:
            {overview_content}

            Extract and organize:
            1. Core workflow stages (1-7)
            2. Technology stack components
            3. Key features and capabilities
            4. Processing pipeline architecture
            5. Input/output specifications
            6. Module relationships and dependencies
            """

            response = completion(
                model="gpt-4o",
                messages=[{"role": "user", "content": system_prompt}]
            )

            print("✅ System overview ingested successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to ingest system overview: {e}")
            return False

    def learn_module_details(self, module_name: str, module_content: str):
        """Learn specific module details and capabilities"""
        if module_name not in self.memori_instances:
            print(f"❌ Module {module_name} not found in configuration")
            return False

        memori = self.memori_instances[module_name]

        try:
            module_prompt = f"""
            You are learning about the {module_name} module in the Video Processor system.

            Module Information:
            {module_content}

            Analyze and remember:
            1. Module purpose and functionality
            2. Technical implementation details
            3. Input/output specifications
            4. Dependencies and integrations
            5. Configuration parameters
            6. Common use cases and scenarios
            7. Troubleshooting information
            8. Performance considerations
            """

            response = completion(
                model="gpt-4o",
                messages=[{"role": "user", "content": module_prompt}]
            )

            print(f"✅ Learned details for module: {module_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to learn module details for {module_name}: {e}")
            return False

    def demonstrate_real_time_memory(self):
        """Demonstrate real-time memory functionality"""
        print("\n🎯 REAL-TIME MEMORY DEMONSTRATION")
        print("=" * 50)

        # Test queries that show memory intelligence
        test_scenarios = [
            {
                "scenario": "New developer onboarding",
                "query": "How does the video processing system work from start to finish?",
                "context": "A new developer needs to understand the complete workflow"
            },
            {
                "scenario": "Troubleshooting video upload issue",
                "query": "What could cause video upload to fail and how do I fix it?",
                "context": "User is having trouble uploading MP4 files"
            },
            {
                "scenario": "Performance optimization",
                "query": "How can I optimize the OCR processing for better performance?",
                "context": "System is slow with large video files"
            },
            {
                "scenario": "Integration between modules",
                "query": "How does frame extraction connect to OCR processing?",
                "context": "Need to understand data flow between modules"
            },
            {
                "scenario": "Rule application debugging",
                "query": "Why are my business rules not being applied correctly?",
                "context": "Generated manual doesn't match expected format"
            }
        ]

        for i, test in enumerate(test_scenarios, 1):
            print(f"\n{i}. {test['scenario']}")
            print(f"   Query: {test['query']}")
            print(f"   Context: {test['context']}")

            # Query main memory for comprehensive response
            insights = self.memori_instances["main"].retrieve_context(test["query"], limit=5)

            print(f"   📊 Memory Response: Found {len(insights)} relevant insights")
            if insights:
                print(f"   💡 Key Insight: {insights[0].get('content', 'N/A')[:100]}...")

    def show_pipeline_intelligence(self):
        """Show how memory understands the processing pipeline"""
        print("\n🔄 PROCESSING PIPELINE INTELLIGENCE")
        print("=" * 50)

        pipeline_queries = [
            "Explain the complete workflow from video upload to manual generation",
            "What happens during frame extraction and why is it important?",
            "How does OCR processing convert images to structured text?",
            "What role does the chain-of-thought module play in deduplication?",
            "How do business rules get applied to generate the final manual?"
        ]

        for i, query in enumerate(pipeline_queries, 1):
            print(f"\n{i}. Pipeline Stage Understanding")
            print(f"   {query}")

            # Query across relevant modules
            insights = self.memori_instances["main"].retrieve_context(query, limit=3)

            print(f"   📊 Memory Analysis: {len(insights)} pipeline insights found")
            if insights:
                for j, insight in enumerate(insights[:2], 1):
                    print(f"   {j}. {insight.get('content', 'N/A')[:120]}...")

    def demonstrate_cross_module_queries(self):
        """Demonstrate queries that span multiple modules"""
        print("\n🔗 CROSS-MODULE INTELLIGENCE")
        print("=" * 50)

        cross_module_queries = [
            {
                "question": "How do I troubleshoot when OCR quality is poor?",
                "modules_involved": ["ocr_processing", "frame_extraction", "quality_analysis"],
                "context": "Need to understand the relationship between image quality and OCR accuracy"
            },
            {
                "question": "What's the best way to handle large video files?",
                "modules_involved": ["video_input", "parallel_processing", "video_storage"],
                "context": "Performance optimization for large files across the system"
            },
            {
                "question": "How do I customize the Excel manual output format?",
                "modules_involved": ["rule_application", "manual_generation", "llm_processing"],
                "context": "Need to modify business rules and templates for different clients"
            }
        ]

        for test in cross_module_queries:
            print(f"\n❓ {test['question']}")
            print(f"   🔧 Involves: {', '.join(test['modules_involved'])}")
            print(f"   📝 Context: {test['context']}")

            # Query main memory for cross-module understanding
            insights = self.memori_instances["main"].retrieve_context(test["question"], limit=4)

            print(f"   📊 Cross-module analysis: {len(insights)} connections found")
            if insights:
                print(f"   💡 Key connection: {insights[0].get('content', 'N/A')[:100]}...")

    def generate_memory_report(self) -> Dict[str, Any]:
        """Generate comprehensive memory report"""
        report = {
            "project_name": self.config.project_name,
            "total_modules": len(self.config.modules),
            "memory_instances": len(self.memori_instances),
            "processing_pipeline": self.config.processing_pipeline,
            "module_categories": {},
            "memory_statistics": {}
        }

        # Categorize modules
        categories = {}
        for module_name, module_info in self.config.modules.items():
            category = module_info.category
            if category not in categories:
                categories[category] = []
            categories[category].append(module_name)

        report["module_categories"] = categories

        # Gather statistics from all memory instances
        for name, memori in self.memori_instances.items():
            try:
                stats = memori.get_memory_stats()
                report["memory_statistics"][name] = stats
            except Exception as e:
                report["memory_statistics"][name] = f"Error: {e}"

        return report


def create_video_processor_config() -> VideoProcessorConfig:
    """Create configuration for the Video Processor project"""

    modules = {
        "video_input": VideoProcessorModule(
            name="video_input",
            category="core",
            priority="critical",
            workflow_stage=1,
            input_types=["video_files"],
            output_types=["validated_video", "metadata"],
            dependencies=["video_storage"],
            technologies=["Flask", "Python"],
            common_issues=["file_format_validation", "size_limits", "upload_timeouts"],
            best_practices=["file_format_validation", "chunked_upload", "progress_tracking"],
            description="Video upload, validation, and initial processing module"
        ),

        "frame_extraction": VideoProcessorModule(
            name="frame_extraction",
            category="core",
            priority="critical",
            workflow_stage=2,
            input_types=["video_files"],
            output_types=["key_frames", "timestamps"],
            dependencies=["video_input"],
            technologies=["OpenCV", "FFmpeg"],
            common_issues=["frame_quality", "extraction_speed", "memory_usage"],
            best_practices=["adaptive_sampling", "quality_thresholds", "memory_optimization"],
            description="Computer vision-based key frame extraction from videos"
        ),

        "ocr_processing": VideoProcessorModule(
            name="ocr_processing",
            category="core",
            priority="critical",
            workflow_stage=3,
            input_types=["key_frames"],
            output_types=["extracted_text", "structured_data"],
            dependencies=["frame_extraction"],
            technologies=["Pytesseract", "PIL"],
            common_issues=["text_accuracy", "language_detection", "image_quality"],
            best_practices=["preprocessing_filters", "multi_language_support", "confidence_scoring"],
            description="Advanced OCR processing to convert frame images to text"
        ),

        "llm_processing": VideoProcessorModule(
            name="llm_processing",
            category="core",
            priority="critical",
            workflow_stage=4,
            input_types=["extracted_text"],
            output_types=["structured_content", "semantic_understanding"],
            dependencies=["ocr_processing"],
            technologies=["OpenAI_GPT", "LangChain"],
            common_issues=["token_limits", "context_understanding", "cost_optimization"],
            best_practices=["context_management", "prompt_engineering", "response_validation"],
            description="AI-powered content generation and structuring using OpenAI GPT"
        ),

        "chain_of_thought": VideoProcessorModule(
            name="chain_of_thought",
            category="core",
            priority="high",
            workflow_stage=5,
            input_types=["structured_content"],
            output_types=["deduplicated_content", "semantic_analysis"],
            dependencies=["llm_processing"],
            technologies=["semantic_similarity", "embedding_analysis"],
            common_issues=["duplicate_detection", "semantic_accuracy", "processing_time"],
            best_practices=["similarity_thresholds", "context_awareness", "incremental_processing"],
            description="Deduplication and semantic analysis with chain-of-thought reasoning"
        ),

        "rule_application": VideoProcessorModule(
            name="rule_application",
            category="core",
            priority="high",
            workflow_stage=6,
            input_types=["deduplicated_content"],
            output_types=["validated_content", "formatted_output"],
            dependencies=["chain_of_thought"],
            technologies=["business_rules_engine", "version_control"],
            common_issues=["rule_conflicts", "version_management", "validation_errors"],
            best_practices=["rule_testing", "version_control", "conflict_resolution"],
            description="Dynamic business rule application and versioning system"
        ),

        "manual_generation": VideoProcessorModule(
            name="manual_generation",
            category="core",
            priority="critical",
            workflow_stage=7,
            input_types=["validated_content"],
            output_types=["excel_manual", "structured_document"],
            dependencies=["rule_application"],
            technologies=["pandas", "openpyxl", "template_engine"],
            common_issues=["format_consistency", "template_errors", "data_mapping"],
            best_practices=["template_validation", "format_standards", "error_handling"],
            description="Excel manual creation with structured worksheets and formatting"
        )
    }

    return VideoProcessorConfig(
        project_name="Video Processor - Operational Video Manual Generation",
        modules=modules,
        base_namespace="video_processor",
        processing_pipeline=[
            "video_input",
            "frame_extraction",
            "ocr_processing",
            "llm_processing",
            "chain_of_thought",
            "rule_application",
            "manual_generation"
        ],
        memory_modes={
            "conscious_ingest": True,
            "auto_ingest": True
        },
        retention_policies={
            "critical": "permanent",
            "high": "2_years",
            "medium": "1_year",
            "low": "6_months"
        }
    )


async def main():
    """Main function for Video Processor memory building"""
    print("🎥 Video Processor Memory Builder")
    print("=" * 60)

    # Create project configuration
    config = create_video_processor_config()

    print(f"📋 Project: {config.project_name}")
    print(f"📊 Total Modules: {len(config.modules)}")
    print(f"🔄 Processing Pipeline: {len(config.processing_pipeline)} stages")
    print(f"🏗️ Memory Architecture: {config.base_namespace}")
    print()

    # Initialize memory builder
    builder = VideoProcessorMemoryBuilder(config)
    builder.enable_all_memories()

    print("\n" + "=" * 60)
    print("🧠 MEMORY BUILDING PHASES")
    print("=" * 60)

    # Phase 1: System Overview Ingestion
    print("\n📚 Phase 1: System Overview Ingestion")
    system_overview = """
    Video Processor is an AI-powered system that creates operational user manuals from videos.

    Core Workflow:
    1. Video Input: Upload operational videos (MP4, AVI, MOV, etc.)
    2. Frame Extraction: Extract key frames using computer vision
    3. OCR Processing: Convert images to text using advanced OCR
    4. LLM Processing: Generate structured content using AI
    5. Chain-of-Thought: Apply deduplication and semantic analysis
    6. Rule Application: Apply versioned business rules
    7. Manual Generation: Create structured Excel manuals

    Technology Stack:
    - Backend: Flask, PostgreSQL, MinIO, OpenCV, FFmpeg
    - AI/ML: OpenAI GPT, Pytesseract, Computer Vision
    - Frontend: TailwindCSS, Vanilla JavaScript
    """

    builder.ingest_system_overview(system_overview)

    # Phase 2: Module Learning
    print("\n🎯 Phase 2: Module-Specific Learning")
    for module_name, module_info in config.modules.items():
        print(f"  • Learning: {module_name}")
        module_content = f"""
        Module: {module_info.name}
        Category: {module_info.category}
        Priority: {module_info.priority}
        Description: {module_info.description}
        Workflow Stage: {module_info.workflow_stage}
        Technologies: {', '.join(module_info.technologies)}
        Input Types: {', '.join(module_info.input_types)}
        Output Types: {', '.join(module_info.output_types)}
        Dependencies: {', '.join(module_info.dependencies)}
        Common Issues: {', '.join(module_info.common_issues)}
        Best Practices: {', '.join(module_info.best_practices)}
        """
        builder.learn_module_details(module_name, module_content)

    # Phase 3: Real-Time Demonstrations
    print("\n🎮 Phase 3: Real-Time Memory Demonstrations")
    builder.demonstrate_real_time_memory()
    builder.show_pipeline_intelligence()
    builder.demonstrate_cross_module_queries()

    # Generate final report
    print("\n📊 Generating Memory Report...")
    report = builder.generate_memory_report()

    print("\n" + "=" * 60)
    print("🎉 VIDEO PROCESSOR MEMORY SYSTEM COMPLETE")
    print("=" * 60)

    print(f"📊 Memory Instances: {report['memory_instances']}")
    print(f"🔄 Processing Stages: {len(report['processing_pipeline'])}")
    print(f"📈 Module Categories: {len(report['module_categories'])}")

    print(f"\n🏗️ Architecture Overview:")
    for category, modules in report['module_categories'].items():
        print(f"  • {category}: {len(modules)} modules")

    print("\n✅ Your Video Processor memory system is ready!")
    print("💡 Use real-time queries to explore the system intelligence!")


if __name__ == "__main__":
    asyncio.run(main())
