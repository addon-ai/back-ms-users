"""
Main schema generator orchestrating the entire generation process.
"""
import getpass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from openapi_processor import OpenApiProcessor
from schema_converter import SchemaConverter
from file_manager import FileManager


class SchemaGenerator:
    """Main schema generator for JSON Schema files from OpenAPI specs."""
    
    def __init__(self, output_dir: str = "schemas"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.openapi_processor = OpenApiProcessor()
        self.schema_converter = SchemaConverter()
        self.file_manager = FileManager(self.output_dir)
    
    def generate_schemas(self):
        """Generate JSON schemas from OpenAPI specifications."""
        openapi_dirs = self.openapi_processor.find_openapi_directories()
        
        if not openapi_dirs:
            raise Exception("No OpenAPI directories found")
            
        all_schemas = {}
        total_schemas = 0
        
        for openapi_dir in openapi_dirs:
            service_name = openapi_dir.parent.name
            service_schemas = {}
            
            for openapi_file in openapi_dir.glob("*.json"):
                if "openapi" in openapi_file.name.lower():
                    schemas = self.schema_converter.extract_schemas_from_openapi(openapi_file)
                    service_schemas.update(schemas)
            
            if service_schemas:
                all_schemas[service_name] = service_schemas
                self.file_manager.save_individual_schemas(service_schemas, service_name)
                total_schemas += len(service_schemas)
            
        if all_schemas:
            self.file_manager.save_combined_schemas(all_schemas)
            
        return total_schemas, len(all_schemas)
    
    def generate_summary_report(self) -> None:
        """Generate a summary report of generated schemas."""
        report = {
            "generation_summary": {
                "timestamp": datetime.now().isoformat(),
                "generator": "OpenAPI to JSON Schema Generator",
                "version": "1.0.0",
                "user": getpass.getuser()
            },
            "services": {},
            "total_schemas": 0
        }
        
        for service_dir in self.output_dir.iterdir():
            if service_dir.is_dir() and service_dir.name != "__pycache__":
                schema_files = list(service_dir.glob("*.json"))
                if schema_files:
                    report["services"][service_dir.name] = {
                        "schema_count": len(schema_files),
                        "schemas": [f.stem for f in schema_files]
                    }
                    report["total_schemas"] += len(schema_files)
        
        self.file_manager.save_report(report)