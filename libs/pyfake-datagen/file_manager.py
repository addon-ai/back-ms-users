"""
File manager for handling fake data file operations.
"""
import json
from pathlib import Path
from typing import Dict

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

logger = get_logger(__name__)


class FileManager:
    """Handles file operations for fake data generation."""
    
    def save_fake_data(self, fake_data: Dict, output_file: Path) -> None:
        """Save fake data to a JSON file."""
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(fake_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved fake data: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to save fake data to {output_file}: {e}")