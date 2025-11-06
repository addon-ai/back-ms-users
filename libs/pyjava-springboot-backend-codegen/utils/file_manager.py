"""
File system operations manager for code generation.
"""
from pathlib import Path
from typing import Dict, Any


class FileManager:
    """Handles file system operations for code generation."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
    
    def get_package_path(self, package_name: str) -> Path:
        """
        Convert package name to file system path.
        
        Args:
            package_name: Java package name (e.g., 'com.example.service')
            
        Returns:
            Path object representing the directory structure
        """
        return Path("src/main/java") / package_name.replace(".", "/")
    
    def get_test_package_path(self, package_name: str) -> Path:
        """
        Convert package name to test file system path.
        
        Args:
            package_name: Java package name (e.g., 'com.example.service')
            
        Returns:
            Path object representing the test directory structure
        """
        return Path("src/test/java") / package_name.replace(".", "/")
    
    def create_test_directories(self):
        """
        Create standard Maven test directory structure.
        """
        test_dirs = [
            Path("src/test/java"),
            Path("src/test/resources")
        ]
        
        for test_dir in test_dirs:
            full_path = self.output_dir / test_dir
            self.ensure_directory(full_path)
    
    def ensure_directory(self, path: Path):
        """
        Create directory if it doesn't exist.
        
        Args:
            path: Path object representing the directory to create
        """
        path.mkdir(parents=True, exist_ok=True)
    
    def write_file(self, file_path: Path, content: str):
        """
        Write content to file, creating directories as needed.
        
        Args:
            file_path: Path where the file will be written
            content: String content to write to the file
        """
        self.ensure_directory(file_path.parent)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Generated: {file_path}")
    
    def check_dto_exists(self, dto_base_path: Path, dto_name: str) -> bool:
        """
        Check if a DTO file exists.
        
        Args:
            dto_base_path: Base path to the DTO directory
            dto_name: Name of the DTO class
            
        Returns:
            True if the DTO file exists, False otherwise
        """
        dto_file_path = dto_base_path / f'{dto_name}.java'
        return dto_file_path.exists()