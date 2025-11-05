"""
JSF (JSON Schema Faker) generator for creating fake data from JSON schemas.
"""
import json
from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.logging_setup import get_logger

logger = get_logger(__name__)

try:
    from jsf import JSF
    JSF_AVAILABLE = True
except ImportError:
    JSF_AVAILABLE = False
    logger.warning("⚠️ jsf library not found, install with: pip install jsf")

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    logger.warning("⚠️ faker library not found, install with: pip install faker")


class JSFGenerator:
    """Generates fake data using JSON Schema Faker (jsf) Python library."""
    
    def __init__(self):
        if not JSF_AVAILABLE:
            logger.error("❌ jsf library is required. Install with: pip install jsf")
            raise ImportError("jsf library not available")
        if not FAKER_AVAILABLE:
            logger.error("❌ faker library is required. Install with: pip install faker")
            raise ImportError("faker library not available")
        logger.info("✅ jsf and faker libraries are available")
        self.faker = Faker()
    
    def generate_from_schema(self, schema_file: Path) -> Optional[Dict]:
        """Generate fake data from a JSON schema file."""
        try:
            logger.debug(f"Generating fake data for: {schema_file}")
            
            # Load the schema
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Resolve $ref if present
            if self._has_unresolved_refs(schema):
                schema = self._resolve_refs(schema, schema_file.parent)
                if not schema:
                    logger.debug(f"Skipping {schema_file.name} - could not resolve $ref")
                    return None
            
            # Generate fake data using JSF first
            jsf_faker = JSF(schema)
            fake_data = jsf_faker.generate()
            
            # Apply custom faker patterns to the generated data
            fake_data = self._apply_custom_fake_data(fake_data, schema)
            
            logger.debug(f"Generated fake data for {schema_file.name}")
            return fake_data
                
        except Exception as e:
            logger.error(f"Error generating fake data for {schema_file}: {e}")
            return None
    
    def _has_unresolved_refs(self, schema: Dict) -> bool:
        """Check if schema contains unresolved $ref."""
        if isinstance(schema, dict):
            if '$ref' in schema and schema['$ref'].startswith('#/'):
                return True
            for value in schema.values():
                if self._has_unresolved_refs(value):
                    return True
        elif isinstance(schema, list):
            for item in schema:
                if self._has_unresolved_refs(item):
                    return True
        return False
    
    def _resolve_refs(self, schema: Dict, schema_dir: Path) -> Optional[Dict]:
        """Resolve $ref references by loading referenced schemas."""
        try:
            if isinstance(schema, dict):
                if '$ref' in schema:
                    ref_path = schema['$ref']
                    if ref_path.startswith('#/components/schemas/'):
                        # Extract schema name from reference
                        ref_schema_name = ref_path.split('/')[-1]
                        ref_file = schema_dir / f"{ref_schema_name}.json"
                        
                        if ref_file.exists():
                            with open(ref_file, 'r', encoding='utf-8') as f:
                                ref_schema = json.load(f)
                            # Remove metadata and return the resolved schema
                            if 'x-metadata' in ref_schema:
                                del ref_schema['x-metadata']
                            return ref_schema
                        else:
                            logger.warning(f"Referenced schema not found: {ref_file}")
                            return None
                else:
                    # Recursively resolve refs in nested objects
                    resolved = {}
                    for key, value in schema.items():
                        if isinstance(value, (dict, list)):
                            resolved_value = self._resolve_refs(value, schema_dir)
                            if resolved_value is not None:
                                resolved[key] = resolved_value
                            else:
                                return None
                        else:
                            resolved[key] = value
                    return resolved
            elif isinstance(schema, list):
                resolved = []
                for item in schema:
                    if isinstance(item, (dict, list)):
                        resolved_item = self._resolve_refs(item, schema_dir)
                        if resolved_item is not None:
                            resolved.append(resolved_item)
                        else:
                            return None
                    else:
                        resolved.append(item)
                return resolved
            else:
                return schema
        except Exception as e:
            logger.error(f"Error resolving refs: {e}")
            return None
    
    def _apply_faker_patterns(self, schema: Dict) -> Dict:
        """Apply faker patterns based on field names."""
        if isinstance(schema, dict):
            if 'properties' in schema:
                for field_name, field_schema in schema['properties'].items():
                    if isinstance(field_schema, dict) and 'type' in field_schema:
                        # Apply patterns based on field name
                        field_lower = field_name.lower()
                        
                        if 'id' in field_lower or field_lower.endswith('id'):
                            field_schema['faker'] = 'datatype.uuid'
                        elif field_lower == 'firstname' or 'firstname' in field_lower:
                            field_schema['faker'] = 'name.firstName'
                        elif field_lower == 'lastname' or 'lastname' in field_lower:
                            field_schema['faker'] = 'name.lastName'
                        elif 'name' in field_lower and 'lastname' not in field_lower and 'firstname' not in field_lower:
                            field_schema['faker'] = 'name.firstName'
                        elif 'date' in field_lower:
                            field_schema['faker'] = 'date.recent'
                        elif field_lower == 'email':
                            field_schema['faker'] = 'internet.email'
                        
                        # Recursively apply to nested objects
                        if 'properties' in field_schema:
                            field_schema = self._apply_faker_patterns(field_schema)
            
            # Handle nested schemas
            for key, value in schema.items():
                if isinstance(value, dict) and key != 'properties':
                    schema[key] = self._apply_faker_patterns(value)
        
        return schema
    
    def _apply_custom_fake_data(self, data: Dict, schema: Dict) -> Dict:
        """Apply custom fake data based on field names."""
        if isinstance(data, dict) and isinstance(schema, dict):
            if 'properties' in schema:
                for field_name, field_value in data.items():
                    if field_name in schema['properties']:
                        field_lower = field_name.lower()
                        
                        if 'id' in field_lower or field_lower.endswith('id'):
                            data[field_name] = str(self.faker.uuid4())
                        elif field_lower == 'firstname' or 'firstname' in field_lower:
                            data[field_name] = self.faker.first_name()
                        elif field_lower == 'lastname' or 'lastname' in field_lower:
                            data[field_name] = self.faker.last_name()
                        elif 'name' in field_lower and 'lastname' not in field_lower and 'firstname' not in field_lower:
                            data[field_name] = self.faker.first_name()
                        elif 'date' in field_lower:
                            data[field_name] = self.faker.date().isoformat() if hasattr(self.faker.date(), 'isoformat') else str(self.faker.date())
                        elif field_lower == 'email':
                            data[field_name] = self.faker.email()
                        elif isinstance(field_value, dict):
                            # Recursively apply to nested objects
                            data[field_name] = self._apply_custom_fake_data(field_value, schema['properties'][field_name])
        
        return data