"""
Schema converter for transforming OpenAPI schemas to JSON Schema format.
"""
import getpass
from datetime import datetime
from pathlib import Path
from typing import Dict

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

from openapi_processor import OpenApiProcessor

logger = get_logger(__name__)


class SchemaConverter:
    """Converts OpenAPI schemas to JSON Schema format."""
    
    def __init__(self):
        self.openapi_processor = OpenApiProcessor()
    
    def _create_metadata(self, source_file: Path) -> Dict:
        """Create x-metadata for generated schemas."""
        return {
            "generatedBy": "OpenAPI to JSON Schema Generator v1.0",
            "generatedFrom": str(source_file.name),
            "generatedAt": datetime.now().isoformat(),
            "generatedBy_user": getpass.getuser(),
            "generator_version": "1.0.0",
            "source_type": "openapi_specification"
        }
    
    def _convert_openapi_schema_to_jsonschema(self, openapi_schema: Dict, title: str = None) -> Dict:
        """Convert OpenAPI schema format to JSON Schema format."""
        json_schema = openapi_schema.copy()
        
        json_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        
        if title:
            json_schema["title"] = title
            
        openapi_specific_fields = ["discriminator", "xml", "externalDocs", "example"]
        for field in openapi_specific_fields:
            json_schema.pop(field, None)
            
        if "nullable" in json_schema:
            if json_schema.get("nullable"):
                current_type = json_schema.get("type")
                if current_type:
                    if isinstance(current_type, list):
                        if "null" not in current_type:
                            current_type.append("null")
                    else:
                        json_schema["type"] = [current_type, "null"]
            json_schema.pop("nullable", None)
            
        if "properties" in json_schema:
            for prop_name, prop_schema in json_schema["properties"].items():
                # Use "id" as title for properties ending with "Id"
                prop_title = "id" if prop_name.endswith("Id") else prop_name
                json_schema["properties"][prop_name] = self._convert_openapi_schema_to_jsonschema(
                    prop_schema, prop_title
                )
                
        if "items" in json_schema:
            json_schema["items"] = self._convert_openapi_schema_to_jsonschema(
                json_schema["items"], "item"
            )
            
        if "additionalProperties" in json_schema and isinstance(json_schema["additionalProperties"], dict):
            json_schema["additionalProperties"] = self._convert_openapi_schema_to_jsonschema(
                json_schema["additionalProperties"], "additional"
            )
            
        return json_schema
    
    def _generate_composite_request_schemas(self, openapi_data: Dict, metadata: Dict) -> Dict[str, Dict]:
        """Generate composite request schemas that include path parameters and request body."""
        composite_schemas = {}
        paths = openapi_data.get("paths", {})
        
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.upper() in ['PUT', 'POST'] and 'requestBody' in operation:
                    operation_id = operation.get('operationId', '')
                    
                    # Only generate for operations that end with known patterns
                    if any(operation_id.startswith(prefix) for prefix in ['Create', 'Update']):
                        composite_schema = self._build_composite_schema(operation, operation_id)
                        if composite_schema:
                            schema_name = f"{operation_id}Request"
                            
                            composite_schema["x-metadata"] = metadata.copy()
                            composite_schema["x-metadata"]["schema_name"] = schema_name
                            composite_schema["x-metadata"]["composite"] = True
                            
                            composite_schemas[schema_name] = composite_schema
        
        return composite_schemas
    
    def _build_composite_schema(self, operation: Dict, operation_id: str) -> Dict:
        """Build a composite schema from path parameters and request body."""
        properties = {}
        required = []
        has_path_params = False
        
        # Add path parameters
        parameters = operation.get('parameters', [])
        for param in parameters:
            if param.get('in') == 'path' and param.get('required'):
                param_name = param['name']
                param_schema = param.get('schema', {'type': 'string'})
                properties[param_name] = param_schema
                required.append(param_name)
                has_path_params = True
        
        # Add request body content if it exists
        request_body = operation.get('requestBody', {})
        if request_body:
            content = request_body.get('content', {})
            json_content = content.get('application/json', {})
            body_schema_ref = json_content.get('schema', {}).get('$ref', '')
            
            if body_schema_ref:
                body_schema_name = body_schema_ref.split('/')[-1]
                
                if has_path_params:
                    # If there are path parameters, wrap the body
                    properties['body'] = {
                        "$ref": body_schema_ref,
                        "title": "body"
                    }
                    required.append('body')
                else:
                    # If no path parameters, use the body schema directly
                    return {
                        "$ref": body_schema_ref,
                        "title": f"{operation_id}Request"
                    }
        
        if not properties:
            return None
        
        return {
            "type": "object",
            "properties": properties,
            "required": required,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": f"{operation_id}Request"
        }
    
    def _expand_refs_in_schemas(self, composite_schemas: Dict[str, Dict], all_schemas: Dict[str, Dict]) -> Dict[str, Dict]:
        """Expand $ref references in composite schemas."""
        expanded_schemas = {}
        
        for schema_name, schema in composite_schemas.items():
            expanded_schema = self._expand_refs_in_schema(schema, all_schemas)
            expanded_schemas[schema_name] = expanded_schema
        
        return expanded_schemas
    
    def _expand_refs_in_schema(self, schema: Dict, all_schemas: Dict[str, Dict]) -> Dict:
        """Recursively expand $ref references in a schema."""
        if isinstance(schema, dict):
            if '$ref' in schema:
                ref_path = schema['$ref']
                if ref_path.startswith('#/components/schemas/'):
                    ref_schema_name = ref_path.split('/')[-1]
                    if ref_schema_name in all_schemas:
                        # Get the referenced schema and expand it
                        ref_schema = all_schemas[ref_schema_name].copy()
                        # Remove OpenAPI-specific fields and keep only JSON Schema fields
                        expanded = self._convert_openapi_schema_to_jsonschema(ref_schema, schema.get('title', ref_schema_name))
                        return expanded
                    else:
                        logger.warning(f"Referenced schema not found: {ref_schema_name}")
                        return schema
                else:
                    return schema
            else:
                # Recursively process nested objects
                expanded = {}
                for key, value in schema.items():
                    expanded[key] = self._expand_refs_in_schema(value, all_schemas)
                return expanded
        elif isinstance(schema, list):
            return [self._expand_refs_in_schema(item, all_schemas) for item in schema]
        else:
            return schema
    
    def extract_schemas_from_openapi(self, openapi_file: Path) -> Dict[str, Dict]:
        """Extract and convert schemas from OpenAPI file."""
        logger.info(f"Processing OpenAPI file: {openapi_file}")
        
        openapi_data = self.openapi_processor.load_json(openapi_file)
        if not openapi_data:
            logger.error(f"Failed to load OpenAPI file: {openapi_file}")
            return {}
            
        schemas = openapi_data.get("components", {}).get("schemas", {})
        if not schemas:
            logger.warning(f"No schemas found in {openapi_file}")
            return {}
            
        converted_schemas = {}
        metadata = self._create_metadata(openapi_file)
        
        # Convert existing schemas
        for schema_name, schema_def in schemas.items():
            json_schema = self._convert_openapi_schema_to_jsonschema(schema_def, schema_name)
            
            json_schema["x-metadata"] = metadata.copy()
            json_schema["x-metadata"]["schema_name"] = schema_name
            json_schema["x-metadata"]["original_file"] = str(openapi_file)
            
            converted_schemas[schema_name] = json_schema
        
        # Generate composite request schemas
        composite_schemas = self._generate_composite_request_schemas(openapi_data, metadata)
        
        # Expand $ref in composite schemas
        expanded_composite_schemas = self._expand_refs_in_schemas(composite_schemas, schemas)
        converted_schemas.update(expanded_composite_schemas)
            
        logger.info(f"Extracted {len(converted_schemas)} schemas from {openapi_file.name}")
        return converted_schemas