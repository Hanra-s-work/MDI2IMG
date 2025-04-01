##
# EPITECH PROJECT, 2024
# MDI2IMG (Workspace)
# File description:
# __main__.py
##

import os
import sys

try:
    from src.main import Main
except ImportError:
    from .src.main import Main

_ERROR = 1
_SUCCESS = 0
_SKIPPED = 3
_SHOW_CONVERTED_IMAGE: bool = True
_CWD = os.path.dirname(os.path.abspath(__file__))
_BINARY_NAME = "MDI2TIF.EXE"
_DEBUG_ENABLED: bool = False
_SPLASH: bool = True

print(f"(mdi2img) module cwd = {_CWD}")

MI = Main(
    success=_SUCCESS,
    error=_ERROR,
    skipped=_SKIPPED,
    show=_SHOW_CONVERTED_IMAGE,
    cwd=_CWD,
    binary_name=_BINARY_NAME,
    debug=_DEBUG_ENABLED,
    splash=_SPLASH
)
MI.const.pdebug("Initialised MDI2IMG module", __name__, _CWD)
status = MI.main()
sys.exit(status)
