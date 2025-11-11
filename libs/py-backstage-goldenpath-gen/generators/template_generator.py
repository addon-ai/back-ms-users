#!/usr/bin/env python3
import os
import pystache

class TemplateGenerator:
    """Generates template.yml for Backstage templates"""
    
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
    
    def generate(self, project_name, config, project_dir):
        """Generate template.yml"""
        template_path = os.path.join(self.templates_dir, "template.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        
        data = {
            'template_id': project_name,
            'template_title': config['project']['general']['description'],
            'template_description': config['project']['general']['description'],
            'stack_type': stack_type,
            'default_owner': 'platform-team',
            'default_groupId': config['project']['params']['configOptions']['basePackage'].rsplit('.', 1)[0],
            'default_artifactId': project_name,
            'default_javaVersion': config['devops']['ci'].get('javaVersion', '21'),
            'default_springBootVersion': '3.2.5',
            'default_coverageThreshold': config['devops']['ci'].get('coverageThreshold', '85'),
            'github_org': config['devops']['github']['organization']
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "template.yml"), 'w') as f:
            f.write(output)
