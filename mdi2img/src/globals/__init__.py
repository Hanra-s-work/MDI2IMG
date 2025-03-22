##
# EPITECH PROJECT, 2024
# MDI2IMG
# File description:
# __init__.py
##

"""
File in charge of linking the ressources that are global knowledge to the program
"""

from . import logo as LOG
from .constants import SUCCESS, ERROR, ERR, TMP_IMG_FOLDER, SELECTED_LIST, SPLASH_NAME, SPLASH, __version__, __author__, Constants

__all__ = [
    "LOG",
    "SUCCESS",
    "ERROR",
    "ERR",
    "TMP_IMG_FOLDER",
    "SELECTED_LIST",
    "SPLASH_NAME",
    "SPLASH",
    "__version__",
    "__author__",
    "Constants"
]
