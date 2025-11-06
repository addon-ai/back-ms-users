"""
Domain layer generation functionality.
"""
from pathlib import Path
from typing import Dict, List, Any


class DomainGenerator:
    """Handles generation of domain layer components."""
    
    def __init__(self, template_renderer, file_manager, property_converter, target_packages, output_dir):
        self.template_renderer = template_renderer
        self.file_manager = file_manager
        self.property_converter = property_converter
        self.target_packages = target_packages
        self.output_dir = output_dir
    
    def generate_entity_status_enum(self, mustache_context: Dict[str, Any]):
        """Generate EntityStatus enum for domain layer."""
        context = mustache_context.copy()
        context.update({
            'packageName': self.target_packages['domain_model'],
            'classname': 'EntityStatus'
        })
        
        content = self.template_renderer.render_template('EntityStatus.mustache', context)
        file_path = self.output_dir / self.file_manager.get_package_path(self.target_packages['domain_model']) / "EntityStatus.java"
        self.file_manager.write_file(file_path, content)
    
    def generate_domain_model(self, entity: str, schema: Dict[str, Any], mustache_context: Dict[str, Any]):
        """Generate domain model (pure POJO) from OpenAPI schema."""
        context = mustache_context.copy()
        
        properties = schema.get('properties', {})
        required_fields = schema.get('required', [])
        
        vars_list = []
        imports = set()
        
        for prop_name, prop_data in properties.items():
            var_info = self.property_converter.convert_openapi_property(prop_name, prop_data, required_fields)
            var_info['hasValidation'] = False
            var_info['validationAnnotations'] = []
            vars_list.append(var_info)
            if var_info.get('import'):
                imports.add(var_info['import'])
        
        context.update({
            'packageName': self.target_packages['domain_model'],
            'classname': entity,
            'vars': vars_list,
            'imports': [{'import': imp} for imp in sorted(imports)],
            'models': [{'model': {'classname': entity, 'vars': vars_list}}],
            'isDomainModel': True,
            'useJPA': False,
            'useLombok': True
        })
        
        content = self.template_renderer.render_template('pojo.mustache', context)
        file_path = self.output_dir / self.file_manager.get_package_path(self.target_packages['domain_model']) / f"{entity}.java"
        self.file_manager.write_file(file_path, content)
    
    def generate_domain_port_output(self, entity: str, mustache_context: Dict[str, Any]):
        """Generate domain repository port (interface)."""
        context = mustache_context.copy()
        context.update({
            'packageName': self.target_packages['domain_ports_output'],
            'classname': f"{entity}RepositoryPort",
            'entityName': entity,
            'entityVarName': entity.lower(),
            'interfaceOnly': True,
            'isDomainPort': True
        })
        
        content = self.template_renderer.render_template('interface.mustache', context)
        file_path = self.output_dir / self.file_manager.get_package_path(self.target_packages['domain_ports_output']) / f"{entity}RepositoryPort.java"
        self.file_manager.write_file(file_path, content)