#!/usr/bin/env python3
"""
Protect Main Repository Remote
Ensures boiler-plate-code-gen remote is always correct
"""

import subprocess
import sys

EXPECTED_REMOTE = "git@github.com:Jiliar/boiler-plate-code-gen.git"

def get_current_remote():
    """Get current remote URL"""
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def fix_remote():
    """Fix remote if incorrect"""
    current = get_current_remote()
    
    if current == EXPECTED_REMOTE:
        print(f"✅ Remote is correct: {EXPECTED_REMOTE}")
        return True
    
    print(f"⚠️  Remote is incorrect: {current}")
    print(f"🔧 Fixing remote to: {EXPECTED_REMOTE}")
    
    try:
        subprocess.run(['git', 'remote', 'set-url', 'origin', EXPECTED_REMOTE], check=True)
        print(f"✅ Remote fixed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fix remote: {e}")
        return False

if __name__ == "__main__":
    if not fix_remote():
        sys.exit(1)
