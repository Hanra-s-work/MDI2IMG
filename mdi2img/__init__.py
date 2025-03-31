"""
File in charge of linking the different elements of the program
"""
import os
from .src import ChangeImageFormat, AVAILABLE_FORMATS, AVAILABLE_FORMATS_HELP, MDIToTiff, ViewImage, LOG, SUCCESS, ERROR, ERR, SELECTED_LIST, SPLASH_NAME, SPLASH, __version__, __author__, Constants, Main

MODULE_CWD = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    "MDIToTiff",
    "ChangeImageFormat",
    "AVAILABLE_FORMATS",
    "AVAILABLE_FORMATS_HELP",
    "ViewImage",
    "LOG",
    "SUCCESS",
    "ERROR",
    "ERR",
    "SELECTED_LIST",
    "SPLASH_NAME",
    "SPLASH",
    "__version__",
    "__author__",
    "Constants",
    "Main",
    "MODULE_CWD"
]
