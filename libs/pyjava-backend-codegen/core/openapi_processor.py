"""
OpenAPI specification processor for extracting schemas and operations.
"""
import json
import glob
from pathlib import Path
from typing import Dict, List, Any, Set


class OpenApiProcessor:
    """Processes OpenAPI specifications and extracts relevant data."""
    
    def __init__(self, project_folder: str):
        self.project_folder = project_folder
    
    def load_openapi_specs(self) -> List[Dict[str, Any]]:
        """
        Load all OpenAPI specifications from Smithy build output.
        
        Returns:
            List of dictionaries containing OpenAPI specifications with metadata
            
        Raises:
            FileNotFoundError: If no OpenAPI spec files are found
        """
        openapi_files = glob.glob(f"build/smithy/{self.project_folder}/openapi/*.openapi.json")
        additional_projections = glob.glob(f"build/smithy/{self.project_folder}-*/openapi/*.openapi.json")
        openapi_files.extend(additional_projections)
        
        if not openapi_files:
            raise FileNotFoundError(f"No OpenAPI spec found for project {self.project_folder}. Run 'smithy build' first.")
        
        specs = []
        for file_path in openapi_files:
            with open(file_path, 'r') as f:
                spec_data = json.load(f)
                service_name = self._extract_service_name_from_path(file_path)
                specs.append({
                    'spec': spec_data,
                    'file_path': file_path,
                    'service_name': service_name
                })
        
        return specs
    
    def _extract_service_name_from_path(self, file_path: str) -> str:
        """
        Extract service name from OpenAPI file path.
        
        Args:
            file_path: Path to the OpenAPI file
            
        Returns:
            Service name in lowercase
        """
        file_name = Path(file_path).stem
        service_name = file_name.replace('.openapi', '')
        
        if service_name.endswith('Service'):
            service_name = service_name[:-7]
        
        return service_name.lower()
    
    def extract_schemas_and_operations(self, openapi_specs: List[Dict[str, Any]]) -> tuple:
        """
        Extract schemas, operations, and entities from OpenAPI specs.
        
        Args:
            openapi_specs: List of OpenAPI specifications
            
        Returns:
            Tuple of (all_schemas, all_operations, all_entities)
        """
        all_schemas = {}
        all_operations = []
        all_entities = set()
        
        for spec_info in openapi_specs:
            openapi_spec = spec_info['spec']
            service_name = spec_info['service_name']
            
            # Extract schemas
            schemas = openapi_spec.get('components', {}).get('schemas', {})
            paths = openapi_spec.get('paths', {})
            
            for schema_name, schema_data in schemas.items():
                all_schemas[f"{service_name}_{schema_name}"] = {
                    'data': schema_data,
                    'service': service_name,
                    'original_name': schema_name
                }
            
            # Extract operations
            for path, methods in paths.items():
                for method, operation_data in methods.items():
                    if 'operationId' in operation_data:
                        all_operations.append({
                            'id': operation_data['operationId'],
                            'service': service_name
                        })
            
            # Extract entities from schemas
            for schema_name in schemas.keys():
                if schema_name.endswith('Response') or schema_name.endswith('ResponseContent'):
                    entity_name = schema_name.replace('Response', '').replace('ResponseContent', '')
                    if entity_name.startswith('Get'):
                        entity_name = entity_name[3:]
                    
                    if entity_name:
                        all_entities.add(entity_name)
        
        return all_schemas, all_operations, list(all_entities)
    
    def group_operations_by_entity(self, all_operations: List[Dict[str, Any]], all_entities: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group operations by entity for consolidated services.
        
        Args:
            all_operations: List of all operations
            all_entities: List of all entities
            
        Returns:
            Dictionary mapping entity names to their operations
        """
        entity_operations = {}
        
        for operation_info in all_operations:
            entity_name = None
            op_id = operation_info['id']
            
            for entity in all_entities:
                if (op_id == f'Create{entity}' or op_id == f'Get{entity}' or 
                    op_id == f'Update{entity}' or op_id == f'Delete{entity}' or 
                    op_id == f'List{entity}s'):
                    entity_name = entity
                    break
            
            if entity_name:
                if entity_name not in entity_operations:
                    entity_operations[entity_name] = []
                entity_operations[entity_name].append(operation_info)
        
        return entity_operations
    
    def find_complex_operations(self, all_operations: List[Dict[str, Any]], entity_operations: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
        """
        Find complex operations for each entity.
        
        Args:
            all_operations: List of all operations
            entity_operations: Operations grouped by entity
            
        Returns:
            Dictionary mapping entity names to their complex operations
        """
        entity_complex_ops = {}
        
        for entity_name in entity_operations.keys():
            complex_operations = []
            for op in all_operations:
                op_id = op['id']
                if (op_id not in [o['id'] for o in entity_operations[entity_name]] and 
                    (op_id.startswith('Get') and 'By' in op_id and 
                     (entity_name.lower() in op_id.lower() or 
                      any(related in op_id for related in ['Cities', 'Countries', 'Regions', 'Neighborhoods']) and entity_name == 'Location'))):
                    complex_operations.append(op_id)
            
            entity_complex_ops[entity_name] = complex_operations
        
        return entity_complex_ops