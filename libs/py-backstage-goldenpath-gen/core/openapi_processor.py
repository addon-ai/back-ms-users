#!/usr/bin/env python3
import os
import json
import shutil

class OpenAPIProcessor:
    """Processes OpenAPI specs from Smithy build output"""
    
    def __init__(self, smithy_build_path="smithy-build.json"):
        self.smithy_build_path = smithy_build_path
    
    def copy_specs(self, project_name, project_dir):
        """Copy OpenAPI specs from Smithy build output"""
        if not os.path.exists(self.smithy_build_path):
            return []
        
        with open(self.smithy_build_path, 'r') as f:
            smithy_build = json.load(f)
        
        projections = smithy_build.get('projections', {})
        openapi_dir = os.path.join(project_dir, 'openapi')
        os.makedirs(openapi_dir, exist_ok=True)
        
        openapi_files = []
        
        for projection_name in projections.keys():
            if projection_name.startswith(project_name.rsplit('-webflux', 1)[0]):
                source_path = os.path.join('build', 'smithy', projection_name, 'openapi')
                
                if os.path.exists(source_path):
                    for file in os.listdir(source_path):
                        if file.endswith('.openapi.json'):
                            src_file = os.path.join(source_path, file)
                            dest_file = os.path.join(openapi_dir, file)
                            shutil.copy2(src_file, dest_file)
                            openapi_files.append(file)
        
        return openapi_files
