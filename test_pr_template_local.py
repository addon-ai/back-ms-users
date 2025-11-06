#!/usr/bin/env python3
"""
Test script for local PR template creation (without GitHub API)
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs', 'pygithub-integration'))

from generators.project_sync_generator import ProjectSyncGenerator

def test_local_pr_template():
    """Test local PR template creation"""
    
    # Create test project directory
    test_project_path = os.path.join(os.path.dirname(__file__), 'test_project')
    os.makedirs(test_project_path, exist_ok=True)
    
    print(f"Testing local PR template creation in: {test_project_path}")
    
    # Initialize project sync generator
    sync_generator = ProjectSyncGenerator()
    
    # Test the local PR template method
    sync_generator._include_pr_template_locally(test_project_path)
    
    # Check if PR template was created
    pr_template_path = os.path.join(test_project_path, '.github', 'pull_request_template.md')
    
    if os.path.exists(pr_template_path):
        print(f"✅ PR template created successfully at: {pr_template_path}")
        
        # Read and display first few lines
        with open(pr_template_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')[:5]
            print("📄 Template content preview:")
            for line in lines:
                print(f"   {line}")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_project_path)
        print(f"🧹 Cleaned up test directory")
        
        return True
    else:
        print(f"❌ PR template not found at: {pr_template_path}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Local PR Template Creation")
    print("=" * 50)
    
    success = test_local_pr_template()
    
    if success:
        print("\n✅ Local PR template test completed successfully!")
    else:
        print("\n❌ Local PR template test failed!")
        sys.exit(1)