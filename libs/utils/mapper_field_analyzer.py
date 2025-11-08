#!/usr/bin/env python3
"""
Mapper Field Analyzer for Dynamic MapStruct Template Generation

This utility analyzes OpenAPI specifications and generates dynamic context
for MapStruct templates to handle unmapped fields automatically.
"""

import json
from typing import Dict, List, Set, Any

class MapperFieldAnalyzer:
    """Analyzes entity fields to generate MapStruct mapping context."""
    
    def __init__(self, openapi_spec: Dict[str, Any]):
        self.openapi_spec = openapi_spec
        self.schemas = openapi_spec.get('components', {}).get('schemas', {})
    
    def analyze_entity_mappings(self, entity_name: str) -> Dict[str, Any]:
        """Analyze entity and generate mapping context for templates."""
        
        # Get entity schemas
        domain_schema = self.schemas.get(entity_name, {})
        create_request_schema = self.schemas.get(f'Create{entity_name}RequestContent', {})
        update_request_schema = self.schemas.get(f'Update{entity_name}RequestContent', {})
        
        # Extract field sets
        domain_fields = set(domain_schema.get('properties', {}).keys())
        create_fields = set(create_request_schema.get('properties', {}).keys())
        update_fields = set(update_request_schema.get('properties', {}).keys())
        
        # Calculate unmapped fields
        unmapped_create_fields = domain_fields - create_fields - {'status', 'createdAt', 'updatedAt', f'{entity_name.lower()}Id'}
        unmapped_update_fields = domain_fields - update_fields - {'status', 'createdAt', 'updatedAt', f'{entity_name.lower()}Id'}
        
        return {
            'unmappedTargetFields': [{'fieldName': field} for field in sorted(unmapped_create_fields)],
            'unmappedUpdateFields': [{'fieldName': field} for field in sorted(unmapped_update_fields)],
            'hasUnmappedFields': len(unmapped_create_fields) > 0 or len(unmapped_update_fields) > 0
        }
    
    def generate_repository_port_context(self, entity_name: str) -> Dict[str, Any]:
        """Generate context for repository port interfaces."""
        return {
            'entityName': entity_name,
            'entityVarName': entity_name.lower(),
            'hasPaginationMethods': True,
            'hasSearchMethods': True
        }

def generate_mapper_context(openapi_file: str, entity_name: str) -> Dict[str, Any]:
    """Generate complete mapper context from OpenAPI specification."""
    
    with open(openapi_file, 'r') as f:
        openapi_spec = json.load(f)
    
    analyzer = MapperFieldAnalyzer(openapi_spec)
    
    # Generate mapping context
    mapping_context = analyzer.analyze_entity_mappings(entity_name)
    repository_context = analyzer.generate_repository_port_context(entity_name)
    
    # Combine contexts
    return {
        **mapping_context,
        **repository_context,
        'entityName': entity_name,
        'entityVarName': entity_name.lower()
    }

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python mapper_field_analyzer.py <openapi_file> <entity_name>")
        sys.exit(1)
    
    openapi_file = sys.argv[1]
    entity_name = sys.argv[2]
    
    context = generate_mapper_context(openapi_file, entity_name)
    print(json.dumps(context, indent=2))