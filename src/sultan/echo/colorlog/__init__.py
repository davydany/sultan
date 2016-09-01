from __future__ import absolute_import
"""
Python-Colorlog is a library created by 'borntyping', and hosted on Github at 
https://github.com/borntyping/python-colorlog using the MIT License. In 
order to keep Sultan non-dependent on other libraries, python-colorlog was 
copied here. 

Please check out Python-Colorlog for your projects!
"""

"""A logging formatter for colored output."""


from sultan.echo.colorlog.colorlog import (
    ColoredFormatter, escape_codes, default_log_colors,
    LevelFormatter)

from sultan.echo.colorlog.logging import (
    basicConfig, root, getLogger, log,
    debug, info, warning, error, exception, critical, StreamHandler)

__all__ = ('ColoredFormatter', 'default_log_colors', 'escape_codes',
           'basicConfig', 'root', 'getLogger', 'debug', 'info', 'warning',
           'error', 'exception', 'critical', 'log', 'exception',
           'StreamHandler', 'LevelFormatter')
