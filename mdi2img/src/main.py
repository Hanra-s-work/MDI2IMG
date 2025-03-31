"""_summary_
    This is a file that will contain the code required to launch a pre-processor for the program
    This is also where input arguments will be managed
"""

import os
import sys
import inspect

from sys import argv
from display_tty import IDISP

from .img_to_tiff import MDIToTiff
from .globals import constants as CONST
from .convert_to_any import AVAILABLE_FORMATS, AVAILABLE_FORMATS_HELP

DEBUG_RULES = ("--debug", "-d", "/d")

_CWD = os.path.dirname(os.path.abspath(__file__))


class Main:
    """_summary_
    This is the main class of the program
    """

    def __init__(self, success: int = CONST.SUCCESS, error: int = CONST.ERROR, show: bool = True, cwd: str = _CWD, debug: bool = False, splash: bool = True) -> None:
        self.argv = argv[1:]
        self.argc = len(self.argv)
        self._display_splash_screen(splash)
        self.success = success
        self.error = error
        self.binary_name = "MDI2TIF.EXE"
        self.debug = debug
        self._check_args()
        self.show = show
        self.src = ""
        self.dest = ""
        self.available_formats = AVAILABLE_FORMATS
        self.dest_found = False
        self.output_format = "default"
        self.cwd = cwd
        self.const = CONST.Constants(
            self.binary_name,
            self.output_format,
            self.cwd,
            self.debug
        )
        if self.dest_found is False:
            self.dest = self.const.temporary_img_folder
        self.mdi_to_tiff_initialised: MDIToTiff = MDIToTiff(
            self.const,
            self.success,
            self.error
        )
        self.class_name = self.__class__.__name__

    def _display_splash_screen(self, display: bool = True) -> None:
        """_summary_
            This is the function that will display the splash screen if authorised to.

        Args:
            display (bool, optional): _description_: The boolean variable that controls the display of the splash screen. Defaults to True.
        """
        if display is True:
            if isinstance(CONST.SPLASH, list):
                for i in CONST.SPLASH:
                    print(i)
            else:
                print(CONST.SPLASH)
            print(f"Splash name: '{CONST.SPLASH_NAME}'")
        print("Welcome to Mdi2Img")

    def _check_output_format(self, output: str) -> str:
        """_summary_
        Check the output format provided by the user and return it if correct.

        Args:
            output (str): _description_: The output provided by the user.

        Returns:
            str: _description_: The format after the check.
        """
        data = output.lower()
        if data in self.available_formats:
            return data
        IDISP.logger.warning(
            "(mdi2img) The format '%s' is not supported, using the default format.",
            f"{data}"
        )
        return self.output_format

    def _disp_version(self) -> None:
        """_summary_
        Display the version of the program
        """
        print(f"The version of this program is: {CONST.__version__}")

    def _help_section(self) -> None:
        """_summary_
        Display the help section of the program
        """
        print("USAGE:")
        msg = f"\t{argv[0]} <<-h>|<-v>|<SRC>> [DEST]"
        msg += "[--debug] [--no-show] [--format=<format>]"
        print(msg)
        print()
        print("KEEP IN MIND:")
        print("When exporting/viewing/saving images, the default output format is tiff.")
        print("Use the --format flag to change the export format.")
        msg = "When no destination is specified, "
        msg += f"the default one is '{CONST.TMP_IMG_FOLDER}'"
        print(msg)
        print()
        print("ARGUMENTS:")
        print(
            "\tINFO: '<argument>' --> required, '[argument]' --> optional '|' --> one or the other"
        )
        print("\t<SRC>            \tMust be either:")
        print("\t                 \t  - a path to an mdi file")
        print("\t                 \t  - a path to a folder containing mdi files")
        print("\t<-h>|<--help>    \tDisplay this help section and exit.")
        print("\t<-v>|<--version> \tDisplay the program's version and exit.")
        print("\t[DEST]           \tMust be either:")
        print("\t                 \t  - the name of the output file")
        print("\t                 \t  - the name of the output folder")
        print(
            "\t[--debug|-d]         \tThis option will display additional information about what the program is doing."
        )
        print(
            "\t[--no-show|-ns]      \tThis option will instruct the program not to display the images once they were converted"
        )
        print(
            "\t[--format=<format>]  \tThis option allows you to change the default output format (tiff)"
        )
        print()
        print("ABOUT:")
        print(f"This program was created by {CONST.__author__}")
        self._disp_version()
        print()
        question = "Do you wish to see a list of the "
        question += f"{len(self.available_formats)} "
        question += "available formats [(y)es/(N)o]: "
        if input(question).lower() in ("y", "yes", "yas", "ye", "ys"):
            print("The available formats are:")
            index = 1
            for i in self.available_formats:
                print(f"\t{index}. '{i}': {AVAILABLE_FORMATS_HELP[i]}")
                index += 1

    def _check_args(self) -> None:
        """_summary_
        Check the arguments passed to the program
        """
        src_found = False
        self.dest_found = False
        if self.argc == 0:
            self._help_section()
            sys.exit(self.error)
        if self.argv[0].lower() in ("-h", "--help", "/?"):
            self._help_section()
            sys.exit(self.success)
        if self.argv[0].lower() in ("-v", "--version", "/v"):
            self._disp_version()
            sys.exit(self.success)
        for i in self.argv:
            arg = i.lower()
            is_path = os.path.exists(i)
            if is_path is True and src_found is False:
                self.src = i
                src_found = True
                continue
            if is_path is True and src_found is True and self.dest_found is False:
                self.dest = i
                self.dest_found = True
                continue
            if is_path is True and self.dest_found is True:
                IDISP.logger.warning(
                    "(mdi2img) Argument '%s' was not expected, ignoring it.",
                    f"{i}"
                )
                continue
            if arg in DEBUG_RULES:
                self.debug = True
                continue
            if arg in ("--no-show", "-ns", "/ns"):
                self.show = True
                continue
            if arg.startswith("--format"):
                self.output_format = self._check_output_format(
                    arg.split("=")[1]
                )
        if src_found is False:
            IDISP.logger.critical(
                "(mdi2img) No source path provided, aborting!"
            )
            sys.exit(self.error)

    def main(self) -> int:
        """_summary_
        This is the main function of this class.

        Returns:
            int: _description_: The return status of the call
        """
        _func_name = inspect.currentframe().f_code.co_name
        if self.debug is True:
            self.const.update_debug(self.debug)
            for i in [
                ("self.src", self.src),
                ("self.dest", self.dest),
                ("self.dest_found", self.dest_found),
                ("self.debug", self.debug),
                ("self.show", self.show),
                ("self.output_format", self.output_format)
            ]:
                self.const.pdebug(
                    f"(main) Variable '{i[0]}' = '{i[1]}'",
                    _func_name,
                    self.class_name
                )
        if os.path.isdir(self.src) is True:
            self.const.pdebug(
                "(main) The provided source path is a folder.",
                _func_name,
                self.class_name
            )
            return self.mdi_to_tiff_initialised.convert_all(
                self.src,
                self.dest,
                self.output_format
            )
        if os.path.isfile(self.src) is True:
            self.const.pdebug(
                "(main) The provided source path is a file",
                _func_name,
                self.class_name
            )
            return self.mdi_to_tiff_initialised.convert(
                self.src,
                self.dest,
                self.output_format
            )
        self.const.pdebug(
            "The provided path does npt correspond to a known type.",
            _func_name,
            self.class_name
        )
        self.const.pcritical(
            f"The source path '{self.src}' does not exist or is neither a folder or a file\nAborting!",
            _func_name,
            self.class_name
        )
        return self.error
