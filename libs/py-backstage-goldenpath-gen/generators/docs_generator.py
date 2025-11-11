#!/usr/bin/env python3
import os
import pystache

class DocsGenerator:
    """Generates documentation files"""
    
    def __init__(self, templates_dir, projects_dir):
        self.templates_dir = templates_dir
        self.projects_dir = projects_dir
    
    def generate_mkdocs(self, project_name, config, project_dir):
        """Generate mkdocs.yml"""
        template_path = os.path.join(self.templates_dir, "project-mkdocs.yml.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        data = {
            'project_name': project_name,
            'project_description': config['project']['general']['description']
        }
        
        output = pystache.render(template, data)
        
        with open(os.path.join(project_dir, "mkdocs.yml"), 'w') as f:
            f.write(output)
    
    def generate_docs_index(self, project_name, docs_dir):
        """Generate docs/index.md from project README.md"""
        readme_path = os.path.join(self.projects_dir, project_name, "README.md")
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            with open(os.path.join(docs_dir, "index.md"), 'w') as f:
                f.write(readme_content)
        else:
            with open(os.path.join(docs_dir, "index.md"), 'w') as f:
                f.write(f"# {project_name}\\n\\nDocumentation coming soon...\\n")
