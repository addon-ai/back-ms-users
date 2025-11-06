#!/usr/bin/env python3
"""
Hexagonal Architecture Spring WebFlux Code Generator

Script for generating reactive Spring Boot applications using Spring WebFlux and R2DBC.
This script serves as a bridge to the pyjava-webflux-backend-codegen library.
"""

import sys
import subprocess
import shutil
from pathlib import Path

# Add the library to the Python path
lib_path = Path(__file__).parent / "pyjava-webflux-backend-codegen"
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "core"))
sys.path.insert(0, str(lib_path / "utils"))
sys.path.insert(0, str(lib_path / "generators"))
sys.path.insert(0, str(Path(__file__).parent))

# Import from the webflux library using direct imports
from config_loader import ConfigLoader
from code_generator import CodeGenerator
from common.logging_setup import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def run_command(cmd: str) -> str:
    """Execute a shell command and return its output."""
    logger.info(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Error: {result.stderr}")
        exit(1)
    return result.stdout


def main():
    """Main entry point for the WebFlux generator."""
    logger.info("📝 Generating OpenAPI from Smithy...")
    run_command("smithy clean")
    run_command("smithy build")
    
    # Clean and create projects directory
    projects_dir = Path("projects")
    if projects_dir.exists():
        shutil.rmtree(projects_dir)
        logger.info("🗑️ Cleaned existing projects directory")
    projects_dir.mkdir(exist_ok=True)
    logger.info("📁 Created projects directory")

    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        logger.info("Usage: python java-webflux-backend-generator.py [templates_dir]")
        logger.info("Example: python java-webflux-backend-generator.py libs/pyjava-webflux-backend-codegen/templates")
        logger.info("Config: libs/config/params-webflux.json (array of project configurations)")
        sys.exit(0)
    
    config_path = "libs/config/params.json"
    templates_dir = sys.argv[1] if len(sys.argv) > 1 else "libs/pyjava-webflux-backend-codegen/templates"
    
    try:
        # Load all project configurations
        all_projects_config = ConfigLoader.load_projects_config(config_path)
        
        # Filter only WebFlux projects
        webflux_projects = [
            project for project in all_projects_config 
            if project['project']['general'].get('type') == 'springWebflux'
        ]
        
        if not webflux_projects:
            logger.info("No WebFlux projects found in configuration")
            return
        
        logger.info(f"Found {len(webflux_projects)} WebFlux project(s) to generate...")
        
        # Generate each WebFlux project
        for i, project_config in enumerate(webflux_projects, 1):
            project_name = project_config['project']['general']['name']
            logger.info(f"[{i}/{len(webflux_projects)}] Generating WebFlux project: {project_name}")
            
            generator = CodeGenerator(config_path, templates_dir, project_config)
            generator.generate_complete_project()
            
        logger.info(f"✅ Successfully generated {len(webflux_projects)} WebFlux project(s)!")
        
    except Exception as e:
        logger.error(f"❌ Error generating WebFlux projects: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
