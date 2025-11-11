#!/usr/bin/env python3
import os
import json
import pystache

class BackstageGoldenPathGenerator:
    def __init__(self, projects_dir="projects", output_dir="backstage-templates", config_path="libs/config/params.json"):
        self.projects_dir = projects_dir
        self.output_dir = output_dir
        self.config_path = config_path
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def generate_all(self):
        """Generate Backstage collection files for all projects"""
        print("🚀 Starting Backstage Collection Generation...")
        
        with open(self.config_path, 'r') as f:
            configs = json.load(f)
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate catalog-info.yaml for each project
        for config in configs:
            project_name = config['project']['general']['name']
            self._generate_project_catalog(project_name, config)
        
        # Generate collection files
        self._generate_collection_components(configs)
        self._generate_mkdocs()
        
        print(f"✅ Backstage collection files generated in {self.output_dir}/")
    
    def _generate_project_catalog(self, project_name, config):
        """Generate catalog-info.yaml for a project"""
        print(f"  📦 Generating catalog for {project_name}...")
        
        project_dir = os.path.join(self.output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        template_path = os.path.join(self.templates_dir, "catalog-info.yaml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        stack_type = config['project']['general'].get('type', 'springBoot')
        
        data = {
            'project_name': project_name,
            'project_description': config['project']['general']['description'],
            'stack_type': stack_type,
            'github_org': config['devops']['github']['organization']
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "catalog-info.yaml"), 'w') as f:
            f.write(output)
    
    def _generate_collection_components(self, configs):
        """Generate collection-components.yml"""
        template_path = os.path.join(self.templates_dir, "collection-components.yml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        targets = []
        for config in configs:
            project_name = config['project']['general']['name']
            targets.append(f"./{project_name}/catalog-info.yaml")
        
        data = {'targets': targets}
        output = pystache.render(template, data)
        
        with open(os.path.join(self.output_dir, "collection-components.yml"), 'w') as f:
            f.write(output)
    
    def _generate_mkdocs(self):
        """Generate mkdocs.yml"""
        template_path = os.path.join(self.templates_dir, "root-mkdocs.yml.mustache")
        if not os.path.exists(template_path):
            return
        
        with open(template_path, 'r') as f:
            template = f.read()
        
        output = pystache.render(template, {})
        
        with open(os.path.join(self.output_dir, "mkdocs.yml"), 'w') as f:
            f.write(output)

if __name__ == "__main__":
    generator = BackstageGoldenPathGenerator()
    generator.generate_all()
