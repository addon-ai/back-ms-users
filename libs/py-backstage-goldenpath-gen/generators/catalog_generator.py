#!/usr/bin/env python3
import os
import pystache

class CatalogGenerator:
    """Generates catalog-info.yml files"""
    
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
    
    def generate_template_catalog(self, project_name, config, project_dir, provides_apis):
        """Generate catalog-info.yml for the template itself"""
        template_path = os.path.join(self.templates_dir, "template-catalog-info.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        stack_type_kebab = 'spring-webflux' if 'webflux' in stack_type.lower() else 'spring-boot'
        
        base_name = project_name.replace('-webflux', '').replace('back-ms-', '')
        system_name = f"{base_name}-system"
        
        data = {
            'template_id': project_name,
            'template_description': config['project']['general']['description'],
            'stack_type_kebab': stack_type_kebab,
            'github_org': config['devops']['github']['organization'],
            'default_owner': 'platform-team',
            'system_name': system_name,
            'provides_apis': provides_apis
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "catalog-info.yml"), 'w') as f:
            f.write(output)
    
    def generate_skeleton_catalog(self, project_name, config, skeleton_dir):
        """Generate skeleton/catalog-info.yml"""
        template_path = os.path.join(self.templates_dir, "catalog-info.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        stack_type_kebab = 'spring-webflux' if 'webflux' in stack_type.lower() else 'spring-boot'
        
        base_name = project_name.replace('-webflux', '').replace('back-ms-', '')
        system_name = f"{base_name}-system"
        
        data = {
            'stack_type_kebab': stack_type_kebab,
            'is_webflux': 'webflux' in stack_type.lower(),
            'system_name': system_name
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(skeleton_dir, "catalog-info.yml"), 'w') as f:
            f.write(output)
