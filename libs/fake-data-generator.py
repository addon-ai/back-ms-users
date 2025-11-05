#!/usr/bin/env python3
"""
Fake Data Generator

Generates fake data from JSON Schema files using jsf (JSON Schema Faker).
Only generates data for Request schemas for unit testing purposes.
"""

import sys
from pathlib import Path

# Add the library to the Python path
lib_path = Path(__file__).parent / "pyfake-datagen"
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(Path(__file__).parent))

# Import components directly
from fake_data_generator import FakeDataGenerator
from common.logging_setup import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def main():
    """Main entry point for the fake data generator."""
    logger.info("🎲 Starting fake data generation from JSON Schemas...")
    
    try:
        generator = FakeDataGenerator()
        generator.generate_fake_data()
        
        logger.info("🎉 Fake data generation completed successfully!")
        
    except Exception as e:
        logger.error(f"💥 Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()