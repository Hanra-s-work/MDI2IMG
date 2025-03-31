##
# EPITECH PROJECT, 2024
# MDI2IMG (Workspace)
# File description:
# __main__.py
##

import os
import sys
from src.main import Main

_ERROR = 1
_SUCCESS = 0
_SHOW_CONVERTED_IMAGE: bool = True
_CWD = os.path.dirname(os.path.abspath(__file__))
_DEBUG_ENABLED: bool = False
_SPLASH: bool = True

print(f"(mdi2img) module cwd = {_CWD}")

MI = Main(
    success=_SUCCESS,
    error=_ERROR,
    show=_SHOW_CONVERTED_IMAGE,
    cwd=_CWD,
    debug=_DEBUG_ENABLED,
    splash=_SPLASH
)
status = MI.main()
sys.exit(status)
