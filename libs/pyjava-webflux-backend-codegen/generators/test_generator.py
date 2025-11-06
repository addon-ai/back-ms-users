"""
Test generation functionality.
"""
from pathlib import Path
from typing import Dict, List, Any


class TestGenerator:
    """Handles generation of test components."""
    
    def __init__(self, template_renderer, file_manager, target_packages, output_dir, openapi_specs):
        self.template_renderer = template_renderer
        self.file_manager = file_manager
        self.target_packages = target_packages
        self.output_dir = output_dir
        self.openapi_specs = openapi_specs
    
    def generate_tests_for_existing_components(self, mustache_context: Dict[str, Any]):
        """Generate tests for all existing mappers, services, and repositories."""
        # Generate mapper tests for all existing mappers
        mapper_dir = self.output_dir / self.file_manager.get_package_path(self.target_packages['application_mapper'])
        if mapper_dir.exists():
            for mapper_file in mapper_dir.glob('*Mapper.java'):
                entity_name = mapper_file.stem.replace('Mapper', '')
                service_name = self._find_service_for_entity(entity_name)
                self.generate_mapper_test(entity_name, service_name, mustache_context)
        
        # Generate service tests for all existing services
        service_dir = self.output_dir / self.file_manager.get_package_path(self.target_packages['application_service'])
        if service_dir.exists():
            for service_file in service_dir.glob('*Service.java'):
                entity_name = service_file.stem.replace('Service', '')
                service_name = self._find_service_for_entity(entity_name)
                operations = self._find_operations_for_entity(entity_name)
                self.generate_service_test(entity_name, service_name, operations, mustache_context)
        
        # Generate repository tests for all existing repositories
        repo_dir = self.output_dir / self.file_manager.get_package_path(self.target_packages['infra_repository'])
        if repo_dir.exists():
            for repo_file in repo_dir.glob('Jpa*Repository.java'):
                entity_name = repo_file.stem.replace('JpaRepository', '').replace('Jpa', '').replace('Repository', '')
                service_name = self._find_service_for_entity(entity_name)
                self.generate_repository_test(entity_name, service_name, mustache_context)
        
        # Generate repository adapter tests for all existing adapters
        adapter_dir = self.output_dir / self.file_manager.get_package_path(self.target_packages['infra_adapter'])
        if adapter_dir.exists():
            for adapter_file in adapter_dir.glob('*RepositoryAdapter.java'):
                entity_name = adapter_file.stem.replace('RepositoryAdapter', '')
                service_name = self._find_service_for_entity(entity_name)
                self.generate_repository_adapter_test(entity_name, service_name, mustache_context)
        
        # Generate controller tests for all existing controllers
        controller_dir = self.output_dir / self.file_manager.get_package_path(self.target_packages['infra_adapters_input_rest'])
        if controller_dir.exists():
            for controller_file in controller_dir.glob('*Controller.java'):
                entity_name = controller_file.stem.replace('Controller', '')
                service_name = self._find_service_for_entity(entity_name)
                operations = self._find_operations_for_entity(entity_name)
                self.generate_controller_test(entity_name, service_name, operations, mustache_context)
    
    def generate_service_test(self, entity: str, service: str, operations: List[Dict[str, Any]], mustache_context: Dict[str, Any]):
        """Generate service unit test."""
        context = mustache_context.copy()
        
        # Build DTO imports and check for actual DTO files
        dto_base_path = self.output_dir / self.file_manager.get_package_path(self.target_packages['application_dto']) / service
        dto_imports = []
        has_create = any(op['id'].startswith('Create') and entity in op['id'] for op in operations)
        has_get = any(op['id'].startswith('Get') and entity in op['id'] for op in operations)
        has_update = any(op['id'].startswith('Update') and entity in op['id'] for op in operations)
        has_delete = any(op['id'].startswith('Delete') and entity in op['id'] for op in operations)
        has_list = any(op['id'] == f'List{entity}s' for op in operations)
        has_delete_dto = self.file_manager.check_dto_exists(dto_base_path, f'Delete{entity}ResponseContent') if has_delete else False
        
        if has_create:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}ResponseContent'
            ])
        if has_get:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.Get{entity}ResponseContent')
        if has_update:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}ResponseContent'
            ])
        if has_delete:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.Delete{entity}ResponseContent')
        if has_list:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.List{entity}sResponseContent')
        
        context.update({
            'packageName': f'{self.target_packages["application_service"]}'.replace('.', '.').replace('main', 'test'),
            'classname': f'{entity}Service',
            'entityName': entity,
            'entityVarName': entity.lower(),
            'hasCreate': has_create,
            'hasGet': has_get,
            'hasUpdate': has_update,
            'hasDelete': has_delete,
            'hasList': has_list,
            'hasDeleteDto': has_delete_dto,
            'dtoImports': dto_imports
        })
        
        content = self.template_renderer.render_template('serviceTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['application_service'])
        file_path = self.output_dir / test_package_path / f'{entity}ServiceTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_repository_test(self, entity: str, service: str, mustache_context: Dict[str, Any]):
        """Generate repository unit test."""
        context = mustache_context.copy()
        
        # Find entity schema to get properties
        entity_schema = None
        for spec_info in self.openapi_specs:
            schemas = spec_info['spec'].get('components', {}).get('schemas', {})
            for schema_name, schema_data in schemas.items():
                if schema_name == f'{entity}Response' or schema_name == f'Get{entity}ResponseContent':
                    entity_schema = schema_data
                    break
            if entity_schema:
                break
        
        # Build properties for test data generation
        properties = []
        if entity_schema:
            schema_properties = entity_schema.get('properties', {})
            required_fields = entity_schema.get('required', [])
            
            for prop_name, prop_data in schema_properties.items():
                if prop_name not in [f'{entity.lower()}Id', 'createdAt', 'updatedAt', 'status']:
                    prop_type = prop_data.get('type', 'string')
                    is_required = prop_name in required_fields
                    
                    # Check actual Java type from property converter
                    java_type = 'String'
                    if prop_type == 'number':
                        if prop_data.get('format') == 'double':
                            java_type = 'Double'
                        else:
                            java_type = 'BigDecimal'
                    elif prop_type == 'integer':
                        java_type = 'Integer'
                    elif prop_type == 'boolean':
                        java_type = 'Boolean'
                    
                    prop_info = {
                        'name': prop_name,
                        'required': is_required,
                        'isString': prop_type == 'string' and 'email' not in prop_name.lower(),
                        'isEmail': 'email' in prop_name.lower(),
                        'isBoolean': prop_type == 'boolean',
                        'isInteger': prop_type == 'integer',
                        'isLong': prop_type == 'integer' and prop_data.get('format') == 'int64',
                        'isDouble': java_type == 'Double',
                        'isBigDecimal': java_type == 'BigDecimal'
                    }
                    properties.append(prop_info)
        
        context.update({
            'packageName': f'{self.target_packages["infra_repository"]}'.replace('.', '.').replace('main', 'test'),
            'entityName': entity,
            'entityVarName': entity.lower(),
            'properties': properties
        })
        
        content = self.template_renderer.render_template('repositoryTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['infra_repository'])
        file_path = self.output_dir / test_package_path / f'Jpa{entity}RepositoryTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_mapper_test(self, entity: str, service: str, mustache_context: Dict[str, Any]):
        """Generate mapper unit test."""
        context = mustache_context.copy()
        
        # Build DTO imports
        dto_base_path = self.output_dir / self.file_manager.get_package_path(self.target_packages['application_dto']) / service
        dto_imports = []
        has_create_dto = self.file_manager.check_dto_exists(dto_base_path, f'Create{entity}RequestContent')
        has_update_dto = self.file_manager.check_dto_exists(dto_base_path, f'Update{entity}RequestContent')
        has_get_dto = self.file_manager.check_dto_exists(dto_base_path, f'Get{entity}ResponseContent')
        
        if has_create_dto:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}ResponseContent'
            ])
        if has_update_dto:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}ResponseContent'
            ])
        if has_get_dto:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.Get{entity}ResponseContent')
        
        # Add response DTO import for toDto and toDtoList methods
        dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.{entity}Response')
        
        context.update({
            'packageName': f'{self.target_packages["application_mapper"]}'.replace('.', '.').replace('main', 'test'),
            'classname': f'{entity}Mapper',
            'entityName': entity,
            'entityVarName': entity.lower(),
            'hasCreateDto': has_create_dto,
            'hasUpdateDto': has_update_dto,
            'hasGetDto': has_get_dto,
            'dtoImports': dto_imports
        })
        
        content = self.template_renderer.render_template('mapperTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['application_mapper'])
        file_path = self.output_dir / test_package_path / f'{entity}MapperTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_controller_test(self, entity: str, service: str, operations: List[Dict[str, Any]], mustache_context: Dict[str, Any]):
        """Generate controller unit test."""
        context = mustache_context.copy()
        
        # Get DTO-specific properties
        create_properties = self._get_dto_properties(f'Create{entity}RequestContent')
        update_properties = self._get_dto_properties(f'Update{entity}RequestContent')
        
        # Build DTO imports
        dto_imports = []
        has_create = any(op['id'].startswith('Create') and entity in op['id'] for op in operations)
        has_get = any(op['id'].startswith('Get') and entity in op['id'] for op in operations)
        has_update = any(op['id'].startswith('Update') and entity in op['id'] for op in operations)
        has_delete = any(op['id'].startswith('Delete') and entity in op['id'] for op in operations)
        has_list = any(op['id'] == f'List{entity}s' for op in operations)
        
        if has_create:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Create{entity}ResponseContent'
            ])
        if has_get:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.Get{entity}ResponseContent')
        if has_update:
            dto_imports.extend([
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}RequestContent',
                f'{self.target_packages["application_dto"]}.{service}.Update{entity}ResponseContent'
            ])
        if has_delete:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.Delete{entity}ResponseContent')
        if has_list:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.List{entity}sResponseContent')
        
        # Find complex operations dynamically from OpenAPI specs
        complex_operations = self._find_complex_operations_for_entity(entity)
        
        # Add DTO imports for complex operations
        for complex_op in complex_operations:
            dto_imports.append(f'{self.target_packages["application_dto"]}.{service}.{complex_op["responseType"]}')
        
        context.update({
            'packageName': f'{self.target_packages["infra_adapters_input_rest"]}'.replace('.', '.').replace('main', 'test'),
            'classname': f'{entity}Controller',
            'entityName': entity,
            'entityVarName': entity.lower(),
            'entityPath': entity.lower() + 's',
            'hasCreate': has_create,
            'hasGet': has_get,
            'hasUpdate': has_update,
            'hasDelete': has_delete,
            'hasList': has_list,
            'complexOperations': complex_operations,
            'dtoImports': dto_imports,
            'createProperties': create_properties,
            'updateProperties': update_properties
        })
        
        content = self.template_renderer.render_template('controllerTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['infra_adapters_input_rest'])
        file_path = self.output_dir / test_package_path / f'{entity}ControllerTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_logging_utils_test(self, mustache_context: Dict[str, Any]):
        """Generate LoggingUtils unit test."""
        context = mustache_context.copy()
        context.update({
            'packageName': f'{self.target_packages["utils"]}'.replace('.', '.').replace('main', 'test'),
            'classname': 'LoggingUtils'
        })
        
        content = self.template_renderer.render_template('LoggingUtilsTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['utils'])
        file_path = self.output_dir / test_package_path / 'LoggingUtilsTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_repository_adapter_test(self, entity: str, service: str, mustache_context: Dict[str, Any]):
        """Generate repository adapter unit test."""
        context = mustache_context.copy()
        context.update({
            'packageName': f'{self.target_packages["infra_adapter"]}'.replace('.', '.').replace('main', 'test'),
            'classname': f'{entity}RepositoryAdapter',
            'entityName': entity,
            'entityVarName': entity.lower(),
            'entityNamePlural': self._pluralize_entity_name(entity)
        })
        
        content = self.template_renderer.render_template('repositoryAdapterTest.mustache', context)
        test_package_path = self.file_manager.get_test_package_path(self.target_packages['infra_adapter'])
        file_path = self.output_dir / test_package_path / f'{entity}RepositoryAdapterTest.java'
        self.file_manager.write_file(file_path, content)
    
    def generate_logback_test_config(self, mustache_context: Dict[str, Any]):
        """Generate logback-test.xml for DEBUG level coverage."""
        context = mustache_context.copy()
        context.update({
            'packageName': f'{self.target_packages["utils"]}'.replace('.', '.').replace('main', 'test')
        })
        
        content = self.template_renderer.render_template('logback-test.xml.mustache', context)
        file_path = self.output_dir / 'src/test/resources/logback-test.xml'
        self.file_manager.write_file(file_path, content)
    
    def _find_service_for_entity(self, entity_name: str) -> str:
        """Find service name for an entity from OpenAPI specs."""
        for spec_info in self.openapi_specs:
            schemas = spec_info['spec'].get('components', {}).get('schemas', {})
            for schema_name in schemas.keys():
                if entity_name in schema_name:
                    return spec_info['service_name']
        return entity_name.lower()
    
    def _find_operations_for_entity(self, entity_name: str) -> List[Dict[str, Any]]:
        """Find operations for an entity from OpenAPI specs."""
        operations = []
        for spec_info in self.openapi_specs:
            paths = spec_info['spec'].get('paths', {})
            for path, methods in paths.items():
                for method, operation_data in methods.items():
                    if 'operationId' in operation_data:
                        op_id = operation_data['operationId']
                        if (op_id.startswith('Create' + entity_name) or 
                            op_id.startswith('Get' + entity_name) or 
                            op_id.startswith('Update' + entity_name) or 
                            op_id.startswith('Delete' + entity_name) or 
                            op_id == f'List{entity_name}s'):
                            operations.append({
                                'id': op_id,
                                'service': spec_info['service_name']
                            })
        return operations
    
    def _find_complex_operations_for_entity(self, entity_name: str) -> List[Dict[str, Any]]:
        """Find complex operations (non-CRUD) for an entity from OpenAPI specs."""
        complex_operations = []
        for spec_info in self.openapi_specs:
            paths = spec_info['spec'].get('paths', {})
            for path, methods in paths.items():
                for method, operation_data in methods.items():
                    if 'operationId' in operation_data:
                        op_id = operation_data['operationId']
                        # Check if it's a complex operation (not basic CRUD)
                        is_basic_crud = (op_id.startswith('Create' + entity_name) or 
                                       op_id.startswith('Get' + entity_name) or 
                                       op_id.startswith('Update' + entity_name) or 
                                       op_id.startswith('Delete' + entity_name) or 
                                       op_id == f'List{entity_name}s')
                        
                        # If it contains the entity name but is not basic CRUD, it's complex
                        if not is_basic_crud and entity_name.lower() in op_id.lower():
                            method_name = op_id[0].lower() + op_id[1:] if op_id else ''
                            response_type = f'{op_id}ResponseContent'
                            
                            complex_operations.append({
                                'operationId': op_id,
                                'methodName': method_name,
                                'responseType': response_type
                            })
        return complex_operations
    
    def _get_dto_properties(self, dto_name: str) -> List[Dict[str, Any]]:
        """Get properties from a specific DTO schema."""
        properties = []
        for spec_info in self.openapi_specs:
            schemas = spec_info['spec'].get('components', {}).get('schemas', {})
            if dto_name in schemas:
                schema_data = schemas[dto_name]
                schema_properties = schema_data.get('properties', {})
                required_fields = schema_data.get('required', [])
                
                for prop_name, prop_data in schema_properties.items():
                    prop_type = prop_data.get('type', 'string')
                    is_required = prop_name in required_fields
                    
                    prop_info = {
                        'name': prop_name,
                        'required': is_required,
                        'isString': prop_type == 'string' and 'email' not in prop_name.lower(),
                        'isEmail': 'email' in prop_name.lower(),
                        'isBoolean': prop_type == 'boolean',
                        'isInteger': prop_type == 'integer'
                    }
                    properties.append(prop_info)
                break
        return properties
    
    def _pluralize_entity_name(self, entity_name: str) -> str:
        """Pluralize entity name with proper English rules."""
        # Handle capitalized entity names (e.g., "City" -> "Cities")
        if entity_name and entity_name[0].isupper():
            lower_name = entity_name.lower()
            if lower_name.endswith('y'):
                plural = lower_name[:-1] + 'ies'
            elif lower_name.endswith(('s', 'sh', 'ch', 'x', 'z')):
                plural = lower_name + 'es'
            else:
                plural = lower_name + 's'
            return plural.capitalize()
        else:
            # Handle lowercase entity names for table names
            if entity_name.endswith('y'):
                return entity_name[:-1] + 'ies'
            elif entity_name.endswith(('s', 'sh', 'ch', 'x', 'z')):
                return entity_name + 'es'
            else:
                return entity_name + 's'