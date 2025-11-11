#!/usr/bin/env python3
import os
import shutil

class SkeletonGenerator:
    """Generates skeleton files"""
    
    def __init__(self, templates_dir, projects_dir):
        self.templates_dir = templates_dir
        self.projects_dir = projects_dir
    
    def generate_readme(self, skeleton_dir):
        """Generate skeleton/README.md"""
        template_path = os.path.join(self.templates_dir, "skeleton-README.md.mustache")
        with open(template_path, 'r') as f:
            template = f.read()
        
        with open(os.path.join(skeleton_dir, "README.md"), 'w') as f:
            f.write(template)
    
    def copy_project_files(self, project_name, skeleton_dir):
        """Copy project files to skeleton excluding .java, .sql, .class, build, target"""
        project_path = os.path.join(self.projects_dir, project_name)
        if not os.path.exists(project_path):
            return
        
        exclude_extensions = {'.java', '.sql', '.class'}
        exclude_dirs = {'build', 'target', '.git', '.idea', '__pycache__'}
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            rel_path = os.path.relpath(root, project_path)
            dest_dir = skeleton_dir if rel_path == '.' else os.path.join(skeleton_dir, rel_path)
            
            os.makedirs(dest_dir, exist_ok=True)
            
            for file in files:
                file_ext = os.path.splitext(file)[1]
                if file_ext not in exclude_extensions:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_dir, file)
                    shutil.copy2(src_file, dest_file)
