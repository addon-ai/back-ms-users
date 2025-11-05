#!/usr/bin/env python3
"""
JSON Schema Generator

Bridge script to the pygenerate-schemasgen library.
This script serves as a bridge to the new modular architecture.
"""

import sys
from pathlib import Path

# Add the library to the Python path
lib_path = Path(__file__).parent / "pygenerate-schemasgen"
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(Path(__file__).parent))

# Import components directly
from schema_generator import SchemaGenerator
from common.logging_setup import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def main():
    """Main entry point for the JSON Schema generator."""
    logger.info("🚀 Starting OpenAPI to JSON Schema generation...")
    
    try:
        generator = SchemaGenerator()
        generator.generate_schemas()
        generator.generate_summary_report()
        
        logger.info("🎉 JSON Schema generation completed successfully!")
        
    except Exception as e:
        logger.error(f"💥 Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()