#!/usr/bin/env python3
import json
import os

class ConfigLoader:
    """Loads and manages configuration from params.json"""
    
    def __init__(self, config_path="libs/config/params.json"):
        self.config_path = config_path
        self.configs = None
    
    def load(self):
        """Load configurations from JSON file"""
        with open(self.config_path, 'r') as f:
            self.configs = json.load(f)
        return self.configs
    
    def get_github_org(self):
        """Get GitHub organization from first config"""
        if not self.configs:
            self.load()
        return self.configs[0]['devops']['github']['organization'] if self.configs else 'addon-ai'
