#!/usr/bin/env python3
"""
Test script for PR template creation
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs', 'pygithub-integration'))

from core.github_client import GitHubClient

def test_pr_template():
    """Test PR template creation"""
    
    # Initialize GitHub client
    github_client = GitHubClient()
    
    # Get authenticated user info
    user_info = github_client.get_user()
    if not user_info:
        print("❌ Failed to get GitHub user info")
        return False
    
    # Test repository details
    owner = user_info.get('login')
    repo_name = "test-pr-template-repo"
    
    print(f"Testing PR template creation for {owner}/{repo_name}")
    
    # Check if repository exists
    if not github_client.repository_exists(owner, repo_name):
        print(f"Repository {owner}/{repo_name} does not exist. Creating...")
        
        # Create test repository (public for personal account)
        repo_data = github_client.create_repository(
            repo_name, 
            "Test repository for PR template functionality",
            private=False
        )
        
        if 'clone_url' not in repo_data:
            print(f"Failed to create repository: {repo_data}")
            return False
        
        print(f"✅ Created repository: {repo_data.get('html_url')}")
    
    # Load PR template content
    template_path = os.path.join(os.path.dirname(__file__), 'libs', 'pyjava-backend-codegen', 'templates', 'project', 'pull_request_template.md')
    
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        print(f"✅ Loaded PR template from: {template_path}")
        
        # Create PR template
        success = github_client.create_pr_template(owner, repo_name, template_content)
        
        if success:
            print(f"✅ Successfully created PR template for {owner}/{repo_name}")
            print(f"🔗 Check it at: https://github.com/{owner}/{repo_name}/.github/pull_request_template.md")
            return True
        else:
            print(f"❌ Failed to create PR template for {owner}/{repo_name}")
            return False
            
    except FileNotFoundError:
        print(f"❌ PR template file not found: {template_path}")
        return False

if __name__ == "__main__":
    print("🧪 Testing PR Template Creation")
    print("=" * 50)
    
    # Check if GitHub token is available
    if not os.getenv('GITHUB_TOKEN'):
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    success = test_pr_template()
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)