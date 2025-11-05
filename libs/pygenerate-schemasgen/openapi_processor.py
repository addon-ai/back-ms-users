"""
OpenAPI file processor for finding and loading OpenAPI specifications.
"""
import json
from pathlib import Path
from typing import List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

logger = get_logger(__name__)


class OpenApiProcessor:
    """Handles OpenAPI file discovery and loading."""
    
    def find_openapi_directories(self) -> List[Path]:
        """Find all OpenAPI directories in the build structure."""
        build_dir = Path("build/smithy")
        if not build_dir.exists():
            logger.error(f"Build directory not found: {build_dir}")
            return []
            
        openapi_dirs = []
        for project_dir in build_dir.iterdir():
            if project_dir.is_dir():
                openapi_dir = project_dir / "openapi"
                if openapi_dir.exists():
                    openapi_dirs.append(openapi_dir)
        
        return openapi_dirs
    
    def load_json(self, file_path: Path) -> dict:
        """Load JSON from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON from {file_path}: {e}")
            return None