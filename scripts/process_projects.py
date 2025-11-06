#!/usr/bin/env python3
"""
Process projects based on their type (springBoot or springWebflux)
"""
import json
import subprocess
import sys
import os

def main():
    config_path = sys.argv[1]
    project_root = sys.argv[2]
    templates_dir = sys.argv[3]
    
    with open(config_path, 'r') as f:
        projects = json.load(f)
    
    for project in projects:
        project_type = project.get('project', {}).get('general', {}).get('type', 'springBoot')
        project_name = project.get('project', {}).get('general', {}).get('name', 'unknown')
        
        print(f'📦 Processing {project_name} (type: {project_type})')
        
        if project_type == 'springBoot':
            generator_script = os.path.join(project_root, 'libs', 'java-springboot-backend-generator.py')
        elif project_type == 'springWebflux':
            generator_script = os.path.join(project_root, 'libs', 'java-webflux-backend-generator.py')
        else:
            print(f'⚠️  Unknown project type: {project_type}. Defaulting to Spring Boot.')
            generator_script = os.path.join(project_root, 'libs', 'java-springboot-backend-generator.py')
        
        if os.path.exists(generator_script):
            result = subprocess.run([sys.executable, generator_script, templates_dir], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f'❌ Error generating {project_name}: {result.stderr}')
                sys.exit(1)
            else:
                print(f'✅ Generated {project_name} successfully')
        else:
            print(f'❌ Generator script not found: {generator_script}')
            if project_type == 'springWebflux':
                print('   Note: Spring WebFlux generator not yet implemented')
            sys.exit(1)

if __name__ == "__main__":
    main()