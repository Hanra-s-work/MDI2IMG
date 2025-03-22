"""
File in charge of converting mdi files to tiff
This extension relies on the windows mdi2tiff program
"""

import os
from typing import Union, List
from ..globals import constants as CONST
from ..convert_to_any import ChangeImageFormat


class MDIToTiff:
    """
    The class in charge of converting an mdi file to a tiff file
        :param success: The exit code of a successful conversion
        :param error: The exit code of a failed conversion
    """

    def __init__(self, binary_name: Union[str, CONST.Constants] = "", success: int = 0, error: int = 1) -> None:
        self.error = error
        self.success = success
        self.skipped = int(error * success)
        if callable(binary_name) is True:
            self.const = binary_name
        else:
            self.const = CONST.Constants(binary_name)
        self.bin_path = self.const.binary_path
        # ------------------- Start Folder conversion stats --------------------
        self.session_active = False
        self.total_items = 0
        self.total_folders = 0
        self.total_nb_of_files = 0
        self.total_files_skipped = 0
        self.total_files_success = 0
        self.total_files_fails = 0
        self.global_status = self.success
        # -------------------- End Folder conversion stats ---------------------
        # ----------------------- Begin image conversion -----------------------
        self.cifi = ChangeImageFormat(
            constants=self.const,
            success=self.success,
            error=self.error
        )
        # ----------------------(- End image conversion -----(------------------

    def _reset_folder_conversion_stats_session(self) -> None:
        """_summary_
        Reset the folder conversion stats
        """
        self.total_items = 0
        self.total_folders = 0
        self.global_status = self.success
        self.session_active = False
        self.total_nb_of_files = 0
        self.total_files_fails = 0
        self.total_files_skipped = 0
        self.total_files_success = 0

    def _initialise_folder_conversion_stat_session(self, folder_content: List[str]) -> None:
        """_summary_
        Set the variables that can be set based on the contents of the folder

        Args:
            folder_content (List[str]): _description_: A list of the content of the input folder.
        """
        self._reset_folder_conversion_stats_session()
        self.total_items = len(folder_content)
        self.total_nb_of_files = self.total_items
        for i in folder_content:
            if os.path.isdir(i) is True:
                self.total_folders += 1
                self.total_nb_of_files -= 1
                continue
        self.session_active = True

    def _update_folder_conversion_stat_session(self, status: int = CONST.SUCCESS) -> None:
        """_summary_
        Update the conversion stats based on the status of the conversion

        Args:
            status (int, optional): _description_: The status of the conversion. Defaults to CONST.SUCCESS.
        """
        if status == self.success:
            self.total_files_success += 1
        elif status == self.skipped:
            self.total_files_skipped += 1
        else:
            self.total_files_fails += 1
            self.global_status = status

    def _display_folder_conversion_stat_session(self) -> None:
        """_summary_
        Display the conversion stats
        """
        self.const.pinfo(f"Total items: {self.total_items}")
        self.const.pinfo(f"Total folders: {self.total_folders}")
        self.const.pinfo(f"Total number of files: {self.total_nb_of_files}")
        self.const.pinfo(f"Total files skipped: {self.total_files_skipped}")
        self.const.pinfo(f"Total files success: {self.total_files_success}")
        self.const.pinfo(f"Total files fails: {self.total_files_fails}")
        if self.global_status == self.success:
            self.const.psuccess("All files have been converted successfully.")
        else:
            self.const.perror("Some files could not be converted.")

    def _run_conversion_steps(self, input_file: str, output_file: str, image_format: str) -> int:
        """_summary_
        This function is the one that will run the different conversion steps that are required in order to achieve the desired format.

        Args:
            input_file (str): _description_: The path to the input file.
            output_file (str): _description_: The path to the output file.
            image_format (str): _description_: The destination format of the image.

        Returns:
            int: _description_: The status of the execution.
        """
        if isinstance(output_file, list) is True:
            step1 = output_file[0]
            step2 = output_file[1]
        else:
            step1 = output_file
            step2 = None
        command = f"{self.bin_path} -source {input_file} -dest {step1} "
        command += f"-log {self.const.log_file_location}"
        exit_code = os.system(command)
        if exit_code != self.success:
            return exit_code
        if step2 is not None:
            return self.cifi.to_desired_format(step1, step2, image_format)
        return exit_code

    def convert(self, input_file: str, output_file: Union[str, List[str]], img_format: str) -> int:
        """_summary_
        Convert an mdi file to a tiff file

        Args:
            input_file (str): _description_: The mdi file to convert
            output_file (Union[str, List[str, str]]): _description_: The tiff file to create

        Returns:
            int: _description_: The status of the convertion (success:int  or error:int)
        """
        if self.session_active is False and self.bin_path is None:
            self.const.err_binary_path_not_found()
            return self.error
        if os.path.exists(input_file) is False:
            self.const.err_item_not_found(
                directory=False,
                item_type="input",
                path=input_file,
                critical=True
            )
            return self.error
        if os.path.exists(output_file) is True:
            self.const.pwarning(f"'{output_file}' already exists, skipping.")
            if self.session_active is True:
                return self.skipped
            return self.success
        checked_output_file = self.cifi._check_output_file(
            output_file,
            img_format
        )
        exit_code = self._run_conversion_steps(
            input_file,
            checked_output_file,
            img_format
        )
        if exit_code == self.success:
            if self.session_active is False:
                msg = f"{input_file} -> {output_file}: ok"
                self.const.psuccess(msg)
            return exit_code
        return self.error

    def convert_all(self, input_directory: str = "", output_directory: str = "", img_format: str = "") -> int:
        """_summary_
        Convert all mdi files in a directory to tiff files

        Args:
            input_directory (str, optional): _description_: The directory containing the mdi files to convert. Defaults to "".
            output_directory (str, optional): _description_: The directory where the tiff files will be created. Defaults to "".

        Returns:
            int: _description_: The status of the convertion (success:int  or error:int)
        """
        if input_directory == "":
            e = self.const.in_directory
            self.const.pwarning(
                f"No input directory was found, defaulting to: '{e}'"
            )
            input_directory = e
        if output_directory == "":
            e = self.const.out_directory
            self.const.pwarning(
                f"No output directory was found, defaulting to: '{e}'"
            )
            output_directory = e
        if self.bin_path is None:
            self.const.err_binary_path_not_found()
            return self.error
        if os.path.exists(input_directory) is False:
            self.const.err_item_not_found(True, "input", input_directory, True)
            return self.error
        if os.path.exists(output_directory) is False:
            try:
                os.makedirs(output_directory)
            except os.error as e:
                self.const.err_item_not_found(
                    True,
                    "output",
                    output_directory,
                    True,
                    additional_text=f"Error: '{e}'"
                )
                return self.error
        dir_content = os.listdir(input_directory)
        self._initialise_folder_conversion_stat_session(dir_content)
        for file in dir_content:
            if file.endswith(".mdi"):
                input_file = os.path.join(input_directory, file)
                output_file = os.path.join(
                    output_directory, file.replace(".mdi", ".tiff")
                )
                self.const.pinfo(
                    f"Converting '{input_file}' to '{output_file}'"
                )
                status = self.convert(input_file, output_file, img_format)
                self._update_folder_conversion_stat_session(status)
                if status == self.success:
                    msg = f"File '{input_file}' has been converted to "
                    msg += f"'{output_file}'."
                    self.const.psuccess(msg)
                elif status == self.skipped:
                    msg = f"File '{input_file}' was skipped."
                    self.const.pinfo(msg)
                else:
                    msg = f"File '{input_file}' could not be converted to "
                    msg += f"'{output_file}'"
                    self.const.perror(msg)
        self._display_folder_conversion_stat_session()
        return self.global_status
