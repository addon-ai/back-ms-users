"""
Schema processor for finding and filtering Request schemas.
"""
from pathlib import Path
from typing import List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

logger = get_logger(__name__)


class SchemaProcessor:
    """Handles schema file discovery and filtering."""
    
    def __init__(self, schemas_dir: Path):
        self.schemas_dir = schemas_dir
    
    def find_request_schemas(self, service_dir: Path) -> List[Path]:
        """Find Request schema files (without Content) in a service directory."""
        request_schemas = []
        
        for schema_file in service_dir.glob("*.json"):
            # Only process Request schemas without Content, not Response schemas
            if ("Request" in schema_file.stem and 
                "Response" not in schema_file.stem and
                "Content" not in schema_file.stem and
                schema_file.stem not in ["all_schemas", "generation_report"]):
                request_schemas.append(schema_file)
                logger.debug(f"Found Request schema: {schema_file}")
        
        logger.info(f"Found {len(request_schemas)} Request schemas in {service_dir.name}")
        return request_schemas