##
# EPITECH PROJECT, 2024
# MDI2IMG (Workspace)
# File description:
# constants.py
##

import os
import platform
from typing import Union
from random import randint
from display_tty import Disp, TOML_CONF
from . import logo as LOG

SUCCESS = 0
ERROR = 1
ERR = ERROR
if platform.system() == "Windows":
    TMP_IMG_FOLDER = "%TEMP%/mdi_to_img_temp"
else:
    TMP_IMG_FOLDER = "/tmp/mdi_to_img_temp"

SELECTED_LIST = LOG.__logo_ascii_art__
SPLASH_NAME = list(SELECTED_LIST)[randint(0, len(SELECTED_LIST) - 1)]
SPLASH = SELECTED_LIST[SPLASH_NAME]

__version__ = "1.0.0"
__author__ = "(c) Henry Letellier"


_CLASS_NAME = "Constants"


class Constants:
    """_summary_
    This is the class that will store general methods and variables that will be used over different classes.
    """

    def __init__(self, binary_name: str = "MDI2TIF.EXE", output_format: str = "default") -> None:
        # ---------------------------- Local global variables ----------------------------
        self.env = os.environ
        self.author = __author__
        self.debug = False
        self.binary_name = binary_name
        self.in_directory = f"{os.getcwd()}/in"
        self.out_directory = f"{os.getcwd()}/out"
        self.out_format = output_format
        self.dttyi = Disp(
            toml_content=TOML_CONF,
            save_to_file=False,
            file_name="",
            file_descriptor=None,
            debug=self.debug,
            logger=None  # self.__class__.__name__
        )
        self.temporary_folder = self._get_temp_folder(self.env)
        self.temporary_img_folder = f"{self.temporary_folder}/mdi_to_img_temp"
        self.log_file_location = f"{self.temporary_folder}/mdi2tiff.log"
        self._create_temp_if_not_present()
        self.binary_path = self._find_mdi2tiff_binary(self.binary_name)
        # ---------------------------- Debug data ----------------------------
        self.pdebug(f"self.env = {self.env}")
        self.pdebug(f"self.author = {self.author}")
        self.pdebug(f"self.debug = {self.debug}")
        self.pdebug(f"self.binary_name = {self.binary_name}")
        self.pdebug(f"self.in_directory = {self.in_directory}")
        self.pdebug(f"self.out_directory = {self.out_directory}")
        self.pdebug(f"self.out_format = {self.out_format}")
        self.pdebug(f"self.temporary_folder = {self.temporary_folder}")
        self.pdebug(f"self.temporary_img_folder = {self.temporary_img_folder}")
        self.pdebug(f"self.log_file_location = {self.log_file_location}")
        self.pdebug(f"self.binary_path = {self.binary_path}")

    def _get_temp_folder(self, env: dict[str, str]) -> str:
        """_summary_
        Check the computer environement to see if the wished key is present.

        Returns:
            str: _description_: The value of the research.
        """
        if "TEMP" in env:
            return env["TEMP"]
        if "TMP" in env:
            return env["TMP"]
        return os.getcwd()

    def _find_mdi2tiff_binary(self, binary_name: str = "MDI2TIF.EXE") -> Union[str, None]:
        """
        Search for the mdi2tiff binary in the module's directory.
        :param binary_name: The name of the binary to locate
        :return:
            str: Full path to the mdi2tiff binary if found, None otherwise.
        """

        self.pdebug(f"Searching for binary: '{binary_name}'")

        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        self.pdebug(f"Current script directory: '{current_script_directory}'")

        binary_path = os.path.join(
            current_script_directory, "bin", binary_name
        )

        self.pdebug(f"Binary path: '{binary_path}'")

        if os.path.exists(binary_path) is True:
            return binary_path
        return None

    def _create_temp_if_not_present(self) -> None:
        """_summary_
        Create the temporary folder if it does not exist.
        """
        self.pdebug(
            f"Temporary export location: '{self.temporary_img_folder}'"
        )
        if os.path.exists(self.temporary_img_folder) is False:
            self.pinfo("Temporary export location does not exist. Creating.")
            try:
                os.makedirs(self.temporary_img_folder, exist_ok=True)
                msg = "Temporary export folder created in: "
                msg += f"'{self.temporary_img_folder}'."
                self.psuccess(msg)
            except os.error as e:
                msg = "Error creating temporary export location ('"
                msg += f"{self.temporary_img_folder}'): {e}"
                self.pcritical(msg)

    def update_debug(self, debug: bool) -> None:
        """_summary_
        Update the debug variable.

        Args:
            debug (bool): _description_: The new debug value.
        """
        self.debug = debug
        self.dttyi.update_disp_debug(debug)

    def perror(self, string: str = "", func_name: str = "perror", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output an error on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        self.dttyi.log_error(string, f"mdi2img::{class_name}::{func_name}")

    def pwarning(self, string: str = "", func_name: str = "pwarning", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output a warning on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        self.dttyi.log_warning(string, f"mdi2img::{class_name}::{func_name}")

    def pcritical(self, string: str = "", func_name: str = "pcritical", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output a critical error on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        self.dttyi.log_critical(string, f"mdi2img::{class_name}::{func_name}")

    def psuccess(self, string: str = "", func_name: str = "psuccess", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output a success message on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        self.dttyi.logger.success(
            string, f"mdi2img::{class_name}::{func_name}")

    def pinfo(self, string: str = "", func_name: str = "pinfo", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output an information message on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        self.dttyi.log_info(string, f"mdi2img::{class_name}::{func_name}")

    def pdebug(self, string: str = "", func_name: str = "pdebug", class_name: str = _CLASS_NAME) -> None:
        """_summary_
        This is a function that will output a debug message on the terminal.

        Args:
            string (str, optional): _description_. Defaults to "".
            func_name (str, optional): _description_. Defaults to "perror".
            class_name (str, optional): _description_. Defaults to the value contained in _CLASS_NAME.
        """
        if self.debug is True:
            self.dttyi.log_debug(string, f"mdi2img::{class_name}::{func_name}")

    def err_item_not_found(self, directory: bool = True,  item_type: str = "input", path: str = '', critical: bool = False, additional_text: str = "") -> None:
        """_summary_
        This is a function that will output an error message when a directory is not found.

        Args:
            directory (bool, optional): _description_: Is the item a directory. Defaults to True.
            item_type (str, optional): _description_: The type of the item.
            path (str, optional): _description_: The path of the directory.
            critical (bool, optional): _description_ Is the message of critical importance. Defaults to True.
        """
        dir_str = "directory"
        if directory is False:
            dir_str = "file"
        msg = f"The {item_type} {dir_str} ('{path}') was not found!"
        msg += f"{additional_text}"
        if critical is True:
            msg += "\n Aborting operation(s)!"
            self.pcritical(msg)
        else:
            self.pwarning(msg)

    def err_binary_path_not_found(self) -> None:
        """_summary_

        Args:
            critical (bool, optional): _description_ Is the message of critical importance. Defaults to True.
        """
        msg = f"Binary path: '{self.binary_path}' was not found."
        msg += "\nAborting operations."
        self.pcritical(msg)
