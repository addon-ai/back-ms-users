"""
PyJava Backend Code Generator

A Python library for generating Java Spring Boot applications following 
Hexagonal Architecture principles from Smithy service definitions.
"""

# Make core components easily accessible
from .core.code_generator import CodeGenerator
from .core.config_loader import ConfigLoader
from .core.openapi_processor import OpenApiProcessor
from .utils.template_renderer import TemplateRenderer
from .utils.file_manager import FileManager
from .utils.property_converter import PropertyConverter

__version__ = "2.0.0"
__author__ = "Jiliar Silgado"

__all__ = [
    "CodeGenerator",
    "ConfigLoader",
    "OpenApiProcessor",
    "TemplateRenderer",
    "FileManager",
    "PropertyConverter"
]