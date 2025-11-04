"""
Main fake data generator orchestrating the entire generation process.
"""
from pathlib import Path
from typing import List

from schema_processor import SchemaProcessor
from jsf_generator import JSFGenerator
from file_manager import FileManager


class FakeDataGenerator:
    """Main fake data generator for creating test data from JSON schemas."""
    
    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)
        
        # Initialize components
        self.schema_processor = SchemaProcessor(self.schemas_dir)
        self.jsf_generator = JSFGenerator()
        self.file_manager = FileManager()
    
    def generate_fake_data(self):
        """Generate fake data for all Request schemas."""
        if not self.schemas_dir.exists():
            raise Exception(f"Schemas directory not found: {self.schemas_dir}")
        
        total_files = 0
        
        # Process each service directory
        for service_dir in self.schemas_dir.iterdir():
            if service_dir.is_dir() and service_dir.name != "__pycache__":
                # Clean existing fake-data directory
                fake_data_dir = service_dir / "fake-data"
                if fake_data_dir.exists():
                    import shutil
                    shutil.rmtree(fake_data_dir)
                
                request_schemas = self.schema_processor.find_request_schemas(service_dir)
                
                if request_schemas:
                    fake_data_dir.mkdir(exist_ok=True)
                    
                    for schema_file in request_schemas:
                        fake_data = self.jsf_generator.generate_from_schema(schema_file)
                        if fake_data:
                            output_file = fake_data_dir / f"{schema_file.stem}.json"
                            self.file_manager.save_fake_data(fake_data, output_file)
                            total_files += 1
        
        return total_files


def main(args=None):
    """Main entry point for the fake data generator."""
    import sys
    
    if args is None:
        args = sys.argv[1:]
    
    if len(args) != 1:
        print("Usage: python fake_data_generator.py <schemas_directory>")
        sys.exit(1)
    
    schemas_dir = args[0]
    
    try:
        generator = FakeDataGenerator(schemas_dir)
        total_files = generator.generate_fake_data()
        print(f"Generated fake data for {total_files} schema files")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()