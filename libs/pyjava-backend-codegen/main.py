"""
Main entry point for the PyJava Backend Code Generator.
"""
import sys
import subprocess
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger, setup_logging

from config_loader import ConfigLoader
from .core.code_generator import CodeGenerator

setup_logging()
logger = get_logger(__name__)


def run_command(cmd: str) -> str:
    """
    Execute a shell command and return its output.
    
    Args:
        cmd: Shell command to execute
        
    Returns:
        Command output as string
        
    Raises:
        SystemExit: If command fails
    """
    logger.info(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Error: {result.stderr}")
        exit(1)
    return result.stdout


def main():
    """
    Main entry point for the generator.
    
    Handles command line arguments, loads configuration, and orchestrates
    the project generation process for multiple projects.
    """
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
        logger.info("Usage: python -m pyjava-backend-codegen [templates_dir]")
        logger.info("Example: python -m pyjava-backend-codegen libs/pyjava-backend-codegen/templates")
        logger.info("Config: libs/config/params.json (array of project configurations)")
        sys.exit(0)
    
    config_path = sys.argv[1] if len(sys.argv) > 1 else "libs/config/params.json"
    templates_dir = str(Path(__file__).parent / "templates")
    
    try:
        # Load all project configurations
        projects_config = ConfigLoader.load_projects_config(config_path)
        
        logger.info(f"Found {len(projects_config)} project(s) to generate...")
        
        # Generate each project
        for i, project_config in enumerate(projects_config, 1):
            project_name = project_config['project']['general']['name']
            logger.info(f"[{i}/{len(projects_config)}] Generating project: {project_name}")
            
            generator = CodeGenerator(config_path, templates_dir, project_config)
            generator.generate_complete_project()
            
        logger.info(f"✅ Successfully generated {len(projects_config)} project(s)!")
        
    except Exception as e:
        logger.error(f"Error generating projects: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()