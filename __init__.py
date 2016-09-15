# -*- coding: utf-8 -*-

"""
This module provides the HtmlTestRunner class, which is heavily based on the
default TextTestRunner.
"""

# Allow version to be detected at runtime.
from .version import __version__

from .runner import HTMLTestRunner

__all__ = ('__version__', 'HTMLTestRunner')
