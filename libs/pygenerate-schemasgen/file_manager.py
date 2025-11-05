"""
File manager for handling schema file operations.
"""
import json
from pathlib import Path
from typing import Dict

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

logger = get_logger(__name__)


class FileManager:
    """Handles file operations for schema generation."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        logger.info(f"Output directory created/verified: {self.output_dir}")
    
    def save_individual_schemas(self, schemas: Dict[str, Dict], service_name: str) -> None:
        """Save individual schema files."""
        service_dir = self.output_dir / service_name
        service_dir.mkdir(parents=True, exist_ok=True)
        
        for schema_name, schema_def in schemas.items():
            schema_file = service_dir / f"{schema_name}.json"
            
            try:
                with open(schema_file, 'w', encoding='utf-8') as f:
                    json.dump(schema_def, f, indent=2, ensure_ascii=False)
                logger.debug(f"Saved schema: {schema_file}")
            except Exception as e:
                logger.error(f"Failed to save schema {schema_file}: {e}")
    
    def save_combined_schemas(self, all_schemas: Dict[str, Dict[str, Dict]]) -> None:
        """Save combined schemas file."""
        combined_file = self.output_dir / "all_schemas.json"
        
        flattened = {}
        for service_name, schemas in all_schemas.items():
            for schema_name, schema_def in schemas.items():
                key = f"{service_name}_{schema_name}"
                flattened[key] = schema_def
                
        try:
            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(flattened, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved combined schemas: {combined_file}")
        except Exception as e:
            logger.error(f"Failed to save combined schemas: {e}")
    
    def save_report(self, report: Dict) -> None:
        """Save generation report."""
        report_file = self.output_dir / "generation_report.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"📊 Generation report saved: {report_file}")
        except Exception as e:
            logger.error(f"Failed to save generation report: {e}")