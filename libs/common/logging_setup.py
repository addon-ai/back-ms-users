#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized logging setup for the Smithy codebase.
Provides a get_logger function for consistent logger configuration across scripts and modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
import os

def setup_logging(level: str = None, stream = sys.stdout, format_str: Optional[str] = None, log_file: Optional[Path] = None):
    """
    Configures the root logger with a consistent format and level.
    Interesting features:
     1. Can be called multiple times (it checks for reentry)
     2. It tries very hard to good module names
     3. Modules included in the log message for easy tracability of code
     4. log level controlled via PYTHONLOGLEVEL env var
    """

    our_level = level
    if level == None:
        our_level = os.getenv('PYTHONLOGLEVEL', 'INFO').upper()

    if logging.getLogger().hasHandlers():
        # Logging is already configured; do not reconfigure.
        return

    if format_str is None:
        format_str = "%(levelname)s - %(name)s - %(message)s"

    handlers = [logging.StreamHandler(stream)]
    if log_file:
        handlers.append( logging.FileHandler(log_file) )

    logging.basicConfig(
        level=our_level,
        format=format_str,
        handlers=handlers,
#        stream=stream
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a logger with the specified name, or the caller's module name if not provided.
    """
    import inspect
    import os
    if name is None or name == "__main__":
        # Use stack to get the caller's filename if run as __main__
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)
        if len(outer_frames) > 1:
            module = inspect.getmodule(outer_frames[1][0])
            if module and hasattr(module, "__file__"):
                name = os.path.splitext(os.path.basename(module.__file__))[0]
            elif module and hasattr(module, "__name__"):
                name = module.__name__
            else:
                name = "__main__"
        else:
            name = "__main__"
    return logging.getLogger(name)
