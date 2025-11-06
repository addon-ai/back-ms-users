"""
DTO generation functionality.
"""
from pathlib import Path
from typing import Dict, List, Any


class DtoGenerator:
    """Handles generation of DTOs and related components."""
    
    def __init__(self, template_renderer, file_manager, property_converter, target_packages, output_dir):
        self.template_renderer = template_renderer
        self.file_manager = file_manager
        self.property_converter = property_converter
        self.target_packages = target_packages
        self.output_dir = output_dir
    
    def generate_dto(self, schema_name: str, schema_data: Dict[str, Any], service_name: str, mustache_context: Dict[str, Any]):
        """Generate application DTOs from OpenAPI schema."""
        context = mustache_context.copy()
        
        properties = schema_data.get('properties', {})
        required_fields = schema_data.get('required', [])
        
        vars_list = []
        imports = set()
        
        for prop_name, prop_data in properties.items():
            var_info = self.property_converter.convert_openapi_property(prop_name, prop_data, required_fields)
            vars_list.append(var_info)
            if var_info.get('import'):
                imports.add(var_info['import'])
        
        dto_package = f"{self.target_packages['application_dto']}.{service_name}"
        
        context.update({
            'packageName': dto_package,
            'classname': schema_name,
            'vars': vars_list,
            'imports': [{'import': imp} for imp in sorted(imports)],
            'models': [{'model': {'classname': schema_name, 'vars': vars_list}}],
            'useBeanValidation': True,
            'useJackson': True
        })
        
        content = self.template_renderer.render_template('pojo.mustache', context)
        file_path = self.output_dir / self.file_manager.get_package_path(dto_package) / f"{schema_name}.java"
        self.file_manager.write_file(file_path, content)
    
    def generate_composite_request_dtos(self, openapi_specs: List[Dict[str, Any]], mustache_context: Dict[str, Any]):
        """Generate composite Request DTOs that include path parameters and request body."""
        for spec_info in openapi_specs:
            openapi_spec = spec_info['spec']
            service_name = spec_info['service_name']
            paths = openapi_spec.get('paths', {})
            
            for path, methods in paths.items():
                for method, operation in methods.items():
                    if method.upper() in ['PUT', 'POST'] and 'requestBody' in operation:
                        operation_id = operation.get('operationId', '')
                        
                        # Only generate for operations that start with Create or Update
                        if any(operation_id.startswith(prefix) for prefix in ['Create', 'Update']):
                            self._generate_composite_request_dto(operation, operation_id, service_name, mustache_context)
    
    def _generate_composite_request_dto(self, operation: Dict, operation_id: str, service_name: str, mustache_context: Dict[str, Any]):
        """Generate a composite Request DTO from path parameters and request body."""
        context = mustache_context.copy()
        
        vars_list = []
        imports = set()
        
        # Add path parameters
        parameters = operation.get('parameters', [])
        for param in parameters:
            if param.get('in') == 'path' and param.get('required'):
                param_name = param['name']
                param_schema = param.get('schema', {'type': 'string'})
                
                var_info = {
                    'name': param_name,
                    'dataType': 'String',
                    'required': True,
                    'hasValidation': True,
                    'validationAnnotations': ['@NotNull']
                }
                vars_list.append(var_info)
        
        # Add request body as a nested object
        request_body = operation.get('requestBody', {})
        content = request_body.get('content', {})
        json_content = content.get('application/json', {})
        body_schema_ref = json_content.get('schema', {}).get('$ref', '')
        
        if body_schema_ref:
            body_schema_name = body_schema_ref.split('/')[-1]
            
            var_info = {
                'name': 'body',
                'dataType': body_schema_name,
                'required': True,
                'hasValidation': True,
                'validationAnnotations': ['@NotNull', '@Valid']
            }
            vars_list.append(var_info)
            
            dto_import = f'{self.target_packages["application_dto"]}.{service_name}.{body_schema_name}'
            imports.add(dto_import)
        
        if not vars_list:
            return
        
        dto_package = f"{self.target_packages['application_dto']}.{service_name}"
        class_name = f"{operation_id}Request"
        
        context.update({
            'packageName': dto_package,
            'classname': class_name,
            'vars': vars_list,
            'imports': [{'import': imp} for imp in sorted(imports)],
            'models': [{'model': {'classname': class_name, 'vars': vars_list}}],
            'useBeanValidation': True,
            'useJackson': True
        })
        
        content = self.template_renderer.render_template('pojo.mustache', context)
        file_path = self.output_dir / self.file_manager.get_package_path(dto_package) / f"{class_name}.java"
        self.file_manager.write_file(file_path, content)