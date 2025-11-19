#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

# Please read README.md, section "Recommanded usage"

import os
import subprocess

from mainwindow import start


def _get_git_version():
    """Get git version information for display at startup."""
    try:
        # Get the directory of this file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Try to get git describe (tag + commits)
        result = subprocess.run(
            ['git', 'describe', '--tags', '--always', '--dirty'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode == 0:
            return result.stdout.strip()
        # Fallback to commit hash
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


# Print git version at startup
git_version = _get_git_version()
if git_version:
    print(f"Git version: {git_version}")
else:
    print("Git version: unknown (not a git repository or git not available)")

start()
