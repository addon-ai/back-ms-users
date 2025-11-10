#!/usr/bin/env python3
"""
Backstage Golden Path Generator
Generates Backstage Software Templates from Java projects
"""
import os
import shutil
import json
from pathlib import Path
import pystache


class BackstageGoldenPathGenerator:
    """Generates Backstage Golden Paths from Java projects."""
    
    def __init__(self, config_path: str):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.projects = json.load(f)
        self.templates_dir = Path(__file__).parent / 'templates'
    
    def generate_all(self, projects_dir: str, output_dir: str):
        """Generate Backstage templates for all projects."""
        projects_path = Path(projects_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        generated_templates = set()
        template_info = []
        
        for project_config in self.projects:
            project_name = project_config['project']['general']['name']
            source_project = projects_path / project_name
            
            if not source_project.exists():
                print(f"⚠️  Project {project_name} not found, skipping...")
                continue
            
            stack_type = 'webflux' if 'webflux' in project_name.lower() else 'springboot'
            template_name = f"{stack_type}-service"
            
            if template_name in generated_templates:
                print(f"⏭️  Skipping {project_name} - {template_name} already generated")
                continue
            
            print(f"📦 Generating Backstage template for {project_name} ({stack_type})...")
            template_data = self.generate_template(source_project, output_path / template_name, project_config, stack_type)
            generated_templates.add(template_name)
            template_info.append(template_data)
        
        if template_info:
            self._generate_root_catalog(output_path, template_info)
    
    def generate_template(self, source_project: Path, output_path: Path, project_config: dict, stack_type: str):
        """Generate a single Backstage template with skeleton."""
        skeleton_path = output_path / 'skeleton'
        if skeleton_path.exists():
            shutil.rmtree(skeleton_path)
        
        def ignore_files(dir, files):
            return [f for f in files if f.endswith(('.java', '.sql')) or f in ('devops', 'target', '.git')]
        
        shutil.copytree(source_project, skeleton_path, ignore=ignore_files)
        
        project_info = project_config['project']
        github_org = project_config.get('devops', {}).get('github', {}).get('organization', 'your-org')
        
        # Generate template.yaml
        template_vars = {
            'template_id': f"{stack_type}-service-template",
            'template_title': f"Java {stack_type.title()} Service",
            'template_description': f"Create a new Java {stack_type.title()} microservice with hexagonal architecture",
            'stack_type': stack_type,
            'default_owner': 'platform-team',
            'default_groupId': project_info['params']['groupId'],
            'default_artifactId': project_info['params']['artifactId'],
            'default_javaVersion': project_config.get('devops', {}).get('ci', {}).get('javaVersion', '21'),
            'default_springBootVersion': project_info['dependencies'].get('springBoot', '3.2.5'),
            'default_coverageThreshold': project_config.get('devops', {}).get('ci', {}).get('coverageThreshold', '85'),
            'github_org': github_org
        }
        
        self._render_template('template.yaml.mustache', output_path / 'template.yaml', template_vars)
        
        # Generate catalog-info.yaml at template level
        self._render_template('template-catalog-info.yaml.mustache', output_path / 'catalog-info.yaml', template_vars)
        
        # Generate catalog-info.yaml for skeleton
        catalog_vars = {
            'system_name': 'backend-services',
            'stack_type': stack_type,
            'is_webflux': stack_type == 'webflux'
        }
        
        self._render_template('catalog-info.yaml.mustache', skeleton_path / 'catalog-info.yaml', catalog_vars)
        
        print(f"✅ Backstage template created at {output_path}")
        
        return {
            'template_id': template_vars['template_id'],
            'template_title': template_vars['template_title'],
            'template_folder': output_path.name
        }
    
    def _render_template(self, template_name: str, output_path: Path, context: dict):
        """Render a Mustache template."""
        template_path = self.templates_dir / template_name
        template_content = template_path.read_text(encoding='utf-8')
        rendered = pystache.render(template_content, context)
        output_path.write_text(rendered, encoding='utf-8')
    
    def _generate_root_catalog(self, output_path: Path, template_info: list):
        """Generate root catalog-info.yaml."""
        github_org = self.projects[0].get('devops', {}).get('github', {}).get('organization', 'your-org')
        
        catalog_content = [
            "apiVersion: backstage.io/v1alpha1",
            "kind: Component",
            "metadata:",
            "  name: hexagonal-architecture-templates",
            "  description: |",
            "    Spring Boot service templates with Hexagonal Architecture (Ports and Adapters).",
            "    Includes both traditional Spring Boot and reactive WebFlux implementations.",
            "  tags:",
            "    - backstage",
            "    - templates",
            "    - java",
            "    - spring-boot",
            "    - webflux",
            "    - hexagonal-architecture",
            "    - microservices",
            "  links:",
            "    - title: Documentation",
            f"      url: https://github.com/{github_org}/backstage-templates/blob/main/README.md",
            "  annotations:",
            f"    github.com/project-slug: {github_org}/backstage-templates",
            f"    backstage.io/techdocs-ref: url:https://github.com/{github_org}/backstage-templates/tree/main",
            "spec:",
            "  type: template-collection",
            "  owner: platform-team",
            "  lifecycle: production"
        ]
        
        catalog_file = output_path / 'catalog-info.yaml'
        catalog_file.write_text('\n'.join(catalog_content), encoding='utf-8')
        
        print(f"\n📋 Root catalog generated: {catalog_file}")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python main.py <config_path> <projects_dir> <output_dir>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    projects_dir = sys.argv[2]
    output_dir = sys.argv[3]
    
    generator = BackstageGoldenPathGenerator(config_path)
    generator.generate_all(projects_dir, output_dir)
    
    print("\n✅ Backstage templates generated successfully!")
    print("\n📚 Structure created:")
    print("   • backstage-templates/catalog-info.yaml")
    print("   • backstage-templates/springboot-service/template.yaml")
    print("   • backstage-templates/springboot-service/skeleton/")
    print("   • backstage-templates/webflux-service/template.yaml")
    print("   • backstage-templates/webflux-service/skeleton/")


if __name__ == '__main__':
    main()
