"""
File in charge of displaying a converted image
"""

import os
import gc
import sys
import tkinter as tk
from platform import system
from PIL.ImageTk import PhotoImage
from typing import Union, Dict
from window_asset_tkinter.window_tools import WindowTools as WT
from window_asset_tkinter.calculate_window_position import CalculateWindowPosition as CWP

if __name__ != "__main__":
    from ..globals import Constants
else:
    cwd = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(cwd, ".."))
    sys.path.append(os.path.join(cwd, "..", ".."))
    sys.path.append(os.path.join(cwd, "..", "..", ".."))
    sys.path.append(os.path.join(cwd, "..", "..", "..", ".."))
    const = os.path.join(cwd, "src", "globals")
    if os.path.exists(const):
        sys.path.append(const)
    from globals import Constants


class ViewImage(WT):
    """
    The class in charge of displaying the image
    """

    def __init__(self, parent_window: tk.Tk = None, width: int = 500, height: int = 400, success: int = 0, error: int = 1, parent_const: Union[Constants, None] = None, debug: bool = False, delay_init: bool = False) -> None:
        """
        The constructor of the class

        :param parent_window: The parent window
        :param width: The width of the window
        :param height: The height of the window
        :param success: The success status code
        :param error: The error status code
        """

        super(ViewImage, self).__init__()

        # Debug status
        self.debug = debug

        # Class name
        self.class_name = self.__class__.__name__

        # Constants
        if isinstance(parent_const, Constants) is True and callable(parent_const) is False:
            self.const: Constants = parent_const
        else:
            self.const: Constants = Constants(
                "",
                "",
                "",
                error,
                success,
                self.debug
            )

        # Status codes
        self.success: int = success
        self.error: int = error
        self.error_message: str = "Error: Path does not exist"
        # Saving width and height of the window
        self.width: int = width
        self.height: int = height
        # Variable to inform if to delay the window initialisation or not
        self.delay_init: bool = delay_init
        # Creating parent window if it does not exist
        self.parent_window = None
        self._check_tkinter_parent_window(parent_window, delay_init=delay_init)
        # Gathering the dimensions of the user's screen to know where to place the window
        self.host_dimensions: Dict[str, int] = None
        self._check_host_screen_dimensions(delay_init=delay_init)
        # Initialising the window position calculator
        self.cwp: CWP = None
        self._check_calculate_window_position(
            host_diemensions=self.host_dimensions,
            width=width,
            height=height,
            delay_init=delay_init
        )
        # Image tracking
        self._images_buffer: list = []
        self.image_data: list = []
        self.max_images: int = 0
        self.current_image: int = 0
        # Window position
        self.x_offset: int = 0
        self.y_offset: int = 0
        # GUI config
        self.bg: str = "white"
        self.fg: str = "black"
        # Title section
        self.title_label: tk.Label = tk.Label
        # image_viewer section
        self.image_viewer: tk.Label = tk.Label
        self.image_viewer_error: tk.Label = tk.Label
        self.has_been_forgotten: bool = False
        # button_prev section
        self.button_prev: tk.Button = tk.Button
        # button_next section
        self.button_next: tk.Button = tk.Button
        # button_open_in_viewer section
        self.button_open_in_viewer: tk.Button = tk.Button
        # The image counter
        self.image_count: tk.Label = tk.Label
        # Current image to be displayed
        self._current_display_image: PhotoImage = None

    def change_width(self, width: int) -> None:
        """
        Change the width of the window

        :param width: The new width of the window
        :return: None
        """
        self.const.pdebug(
            "Changing the width of the window",
            class_name=self.class_name
        )
        self.width = width
        if self.cwp is not None:
            self.cwp.change_width(width)

    def change_height(self, height: int) -> None:
        """
        Change the height of the window

        :param height: The new height of the window
        :return: None
        """
        self.const.pdebug(
            "Changing the height of the window",
            class_name=self.class_name
        )
        self.height = height
        if self.cwp is not None:
            self.cwp.change_height(height)

    def _check_tkinter_parent_window(self, parent_window: Union[tk.Tk, None] = None, delay_init: bool = False) -> None:
        """
        Check if the parent window is a tkinter window

        :return: None
        """
        self.const.pdebug(
            "Checking if the parent window is a tkinter window",
            class_name=self.class_name
        )
        if parent_window is None:
            if delay_init is True:
                self.parent_window = None
            else:
                self.parent_window = self._create_parent_window()
        else:
            self.parent_window = parent_window

    def _check_host_screen_dimensions(self, delay_init: bool = False) -> None:
        """
        Check if the host screen dimensions are set

        :return: None
        """
        self.const.pdebug(
            "Checking if the host screen dimensions are set",
            class_name=self.class_name
        )
        if self.host_dimensions is None:
            if delay_init is True:
                self.host_dimensions = None
                return
            if self.parent_window is None:
                self.parent_window = self._create_parent_window()
            self.host_dimensions = self.get_current_host_screen_dimensions(
                self.parent_window
            )

    def _check_calculate_window_position(self, host_diemensions: dict, width: int, height: int, delay_init: bool = False) -> None:
        """
        Check if the calculate window position is set

        :return: None
        """
        self.const.pdebug(
            "Checking if the calculate window position is set",
            class_name=self.class_name
        )
        if self.cwp is None:
            if delay_init is True:
                self.cwp = None
                return
            if host_diemensions is None:
                self.host_dimensions = self.get_current_host_screen_dimensions(
                    self.parent_window
                )
            if "width" not in host_diemensions or "height" not in host_diemensions:
                return
            self.cwp = CWP(
                host_diemensions["width"],
                host_diemensions["height"],
                width,
                height
            )

    def _create_parent_window(self) -> tk.Tk:
        """
        This is the function in charge of initialising the base window that will be used to render the rest of the software.

        Create the parent window
        :return: The parent window
        """
        self.const.pdebug(
            "Creating the parent window",
            class_name=self.class_name
        )
        window = tk.Tk()
        # window.withdraw()
        return window

    def _load_image(self, image_path_src: str, width: int, height: int) -> dict:
        """
        Load the image into memory

        :param image_path: The path to the image to load
        :return: The image node

        raw_content:
            * "img": <image_instance:obj>
            * "width": <width:int>
            * "height": <height:int>
            * "path": <image_path:str>
            * "name": <image_name:str>
        when error:
            * "name": <the_name:str>
            * "error": <the_error:str>  
        """
        self.const.pinfo(
            f"Loading image: {image_path_src}",
            class_name=self.class_name
        )
        if os.path.exists(image_path_src) is False:
            path_message = {
                "name": image_path_src,
                "error": self.error_message
            }
            self._images_buffer.append(self.error_message)
            self.image_data.append(path_message)
            return path_message
        data = self.load_image(
            image_path=image_path_src,
            width=width,
            height=height
        )
        if "img" in data:
            current_name = image_path_src.replace("\\", "/")
            current_name = current_name.split("/")[-1]
            self._images_buffer.append(data["img"])
            node = {
                "img": data["img"],
                "width": width,
                "height": height,
                "path": image_path_src,
                "name": current_name
            }
            self.image_data.append(node)
            return node
        node = {
            "name": image_path_src,
            "error": data["err_message"]
        }
        self._images_buffer.append(data["err_message"])
        self.image_data.append(node)
        return node

    def _load_images(self, image_paths: list[str], width: int, height: int) -> None:
        """
        Load multiple images into memory

        :param image_paths: The paths to the images to load
        :return: None
        """
        self.const.pdebug(
            "Loading multiple images",
            class_name=self.class_name
        )
        for image_index, image_item in enumerate(image_paths):
            self.const.pdebug(
                f"Loading image {image_index + 1}/{len(image_paths)}: {image_item}",
                class_name=self.class_name
            )
            self._load_image(image_item, width, height)
            self.max_images = image_index

    def _update_current_image_displayed(self) -> None:
        """
        Update the image displayed
        """
        self.const.pdebug(
            "Updating the image displayed",
            class_name=self.class_name
        )
        self.const.pdebug(
            f"Image buffer: {self._images_buffer}",
            class_name=self.class_name
        )
        self.const.pdebug(
            f"Image data: {self.image_data}",
            class_name=self.class_name
        )
        self.const.pdebug(
            f"Current image: {self.current_image}",
            class_name=self.class_name
        )
        if len(self.image_data) > 0 and self.current_image >= len(self.image_data):
            self.current_image = 0
            self.const.pdebug(
                f"Current image: {self.current_image}",
                class_name=self.class_name
            )
        if isinstance(self._images_buffer[self.current_image], str) is True:
            self.const.pdebug(
                f"Image not found: {self._images_buffer[self.current_image]}",
                class_name=self.class_name
            )
            self.image_viewer.pack_forget()
            self.const.pdebug(
                "Disabeling the open in default viewer button",
                class_name=self.class_name
            )
            self.button_open_in_viewer.config(state=tk.DISABLED)
            self.const.pdebug(
                f"Displaying the {self.current_image} image",
                class_name=self.class_name
            )
            self.const.pdebug(
                f"Displaying content of that buffer: {self._images_buffer[self.current_image]}",
                class_name=self.class_name
            )
            image = self._images_buffer[self.current_image]
            self.image_viewer_error.image = image
            self._current_display_image = image
            self.image_viewer_error.config(
                text=image
            )
            self.const.pdebug(
                "Displaying the data",
                class_name=self.class_name
            )
            self.image_viewer_error.pack()
            self.has_been_forgotten = True
            self.const.pdebug(
                "Image not found, displaying error message",
                class_name=self.class_name
            )
            return
        if self.has_been_forgotten is True:
            self.const.pdebug(
                "360: Image has been forgotten",
                class_name=self.class_name
            )
            self.image_viewer_error.pack_forget()
            self.const.pdebug(
                "Image viewer removed",
                class_name=self.class_name
            )
            self.image_viewer.pack(fill=tk.BOTH, expand=True)
            self.const.pdebug(
                "Image viewer displayed",
                class_name=self.class_name
            )
            self.has_been_forgotten = False
            self.const.pdebug(
                "has_been_forgotten has been set to False",
                class_name=self.class_name
            )
        self.const.pdebug(
            f"self.current_image = {self.current_image}",
            class_name=self.class_name
        )
        self.const.pdebug(
            f"Image buffer[{self.current_image}] = {self._images_buffer[self.current_image]}",
            class_name=self.class_name
        )
        image: tk.Image = self._images_buffer[self.current_image]
        self.const.pdebug(
            f"Image data (dir): {dir(image)}",
        )
        self.const.pdebug(
            f"Image (width, height): ({image.width()}, {image.height()})",
            class_name=self.class_name
        )
        for i in dir(image):
            internal_image_data = getattr(image, i)
            if callable(internal_image_data) is True:
                self.const.pdebug(
                    f"Image data (callable): (type): {type(internal_image_data)}: {i}: {internal_image_data}",
                    class_name=self.class_name
                )
            else:
                self.const.pdebug(
                    f"Image data (not callable): (type): {type(internal_image_data)}: {i}: {internal_image_data}",
                    class_name=self.class_name
                )
        if isinstance(image, str) is True:
            self.const.pcritical(
                f"Image is a string: {image}",
                class_name=self.class_name
            )
            return
        self.const.pdebug(
            f"Image data: {image}"
        )
        self.const.pdebug(
            f"Before GC: {gc.get_referrers(self._images_buffer[self.current_image])}",
            class_name=self.class_name
        )
        self.image_viewer.image = image
        self._current_display_image = image
        self.image_viewer.configure(
            image=image
        )
        self.image_viewer.update_idletasks()
        self.const.pdebug(
            "Forcing the update of the image viewer",
            class_name=self.class_name
        )
        self.const.pdebug(
            f"Image data[{self.current_image}] = {self.image_data[self.current_image]}",
            class_name=self.class_name
        )
        self.button_open_in_viewer.config(state=tk.NORMAL)
        self.const.pdebug(
            f"Displaying image: {self.image_data[self.current_image]['name']}",
            class_name=self.class_name
        )

    def _update_current_image_index(self) -> None:
        """
        Update the index displayed of the current image 
        """
        self.const.pdebug(
            "Updating the current image index",
            class_name=self.class_name
        )
        self.image_count.config(
            text=f"Image {self.current_image + 1}/{self.max_images + 1}"
        )

    def _update_current_image_title(self) -> None:
        """
        Update the title of the current image
        """
        self.const.pdebug(
            "Updating the current image title",
            class_name=self.class_name
        )
        self.title_label.config(
            text=self.image_data[self.current_image]["name"]
        )

    def _previous_image(self, *args) -> None:
        """
        Display the previous image and it's name
        :return: None
        """
        self.const.pdebug(
            "Displaying the previous image",
            class_name=self.class_name
        )
        if self.max_images == 0:
            self.image_viewer.config(text="No images to display !")
            return
        if self.current_image > 0:
            self.current_image -= 1
        else:
            self.current_image = self.max_images
        self._update_current_image_displayed()
        self._update_current_image_title()
        self._update_current_image_index()

    def _next_image(self, *args) -> None:
        """
        Display the next image and it's name
        :return: None
        """
        self.const.pdebug(
            "Changing the image",
            class_name=self.class_name
        )
        if self.max_images == 0:
            self.image_viewer.config(text="No images to display !")
            return
        if self.current_image < self.max_images:
            self.current_image += 1
        else:
            self.current_image = 0
        self.const.pdebug(
            f"Current image: {self.current_image}",
            class_name=self.class_name
        )
        self._update_current_image_displayed()
        self._update_current_image_title()
        self._update_current_image_index()

    def hl_swap(self, item1: any, item2: any) -> list[any, any]:
        """
        Swap the values of two items
        :param item1: The first item
        :param item2: The second item
        :return: The items with their values swapped
        """
        self.const.pdebug(
            "Swapping the values of two items",
            class_name=self.class_name
        )
        return [item2, item1]

    def _open_in_system_viewer(self, *args) -> None:
        """
        Open the current image in the system viewer
        :return: None
        """
        self.const.pdebug(
            "Opening the current image in the system viewer",
            class_name=self.class_name
        )
        current_image = self.current_image
        if self.current_image > self.max_images:
            current_image = 0
        if system() == "Windows":
            os.system(
                f"start {self.image_data[current_image]['path']}"
            )
        elif system() == "Linux":
            os.system(
                f"xdg-open {self.image_data[current_image]['path']}"
            )
        elif system() == "Darwin":
            os.system(
                f"open {self.image_data[current_image]['path']}"
            )

    def view(self, image_paths: list[str] | str, width: int = 0, height: int = 0) -> int:
        """
        Display an image
        :param image_path: The path to the image to display
        :return: The status of the display (success:int  or error:int)
        """
        self.const.pdebug(
            "Displaying the image",
            class_name=self.class_name
        )
        button_width = 10
        object_height = 135
        # Pre checks before boot
        self.const.pdebug("Pre checks before boot", class_name=self.class_name)
        self.const.pdebug(
            "Checking the parent window",
            class_name=self.class_name
        )
        self._check_tkinter_parent_window(None, False)
        self.const.pdebug(
            "Checking the host screen dimensions",
            class_name=self.class_name
        )
        self._check_host_screen_dimensions(False)
        self.const.pdebug(
            "Checking the calculate window position",
            class_name=self.class_name
        )
        self._check_calculate_window_position(
            self.host_dimensions,
            width,
            height,
            False
        )
        # Check that the provided width is a number
        self.const.pdebug(
            "Checking the provided width",
            class_name=self.class_name
        )
        if isinstance(width, int) is False:
            self.const.pcritical(
                "The width option needs to be a whole positive number.",
                class_name=self.class_name
            )

        # Check the provided height is a number
        self.const.pdebug(
            "Checking the provided height",
            class_name=self.class_name
        )
        if isinstance(height, int) is False:
            self.const.pcritical(
                "The height option needs to be a whole positive number.",
                class_name=self.class_name
            )

        # Check if the parent window is a tkinter window
        self.const.pdebug(
            "Checking if the parent window is a tkinter window",
            class_name=self.class_name
        )
        if width < 1:
            width = self.width - (button_width*2)
        else:
            width -= button_width*2

        # Check if the height is less than 1
        self.const.pdebug(
            "Checking if the height is less than 1",
            class_name=self.class_name
        )
        if height < 1:
            height = self.height

        # Check if the width are less than 1
        self.const.pdebug(
            "Checking if the width are less than 1",
            class_name=self.class_name
        )
        if width >= self.width:
            width = self.hl_swap(width, self.width)
            self.width = width[-1]+1
            width = width[0]

        # Check if the height is less than 1
        self.const.pdebug(
            "Checking if the height is less than 1",
            class_name=self.class_name
        )
        if height >= self.height:
            height = self.hl_swap(height, self.height)
            self.height = height[-1]+1
            height = height[0]

        # Check if the image path is a string or a list
        if isinstance(image_paths, str) is True:
            self.const.pdebug(
                "The image path is a string, loading single image",
                class_name=self.class_name
            )
            self._load_image(image_paths, width, height)
        elif isinstance(image_paths, list) is True:
            self.const.pdebug(
                "The image path is a list, loading multiple images",
                class_name=self.class_name
            )
            self._load_images(image_paths, width, height)
        else:
            return self.error

        self.const.pdebug(
            "Calculating the center of the users window",
            class_name=self.class_name
        )
        window_coord = self.cwp.calculate_center()

        self.const.pdebug(
            "Initialising a raw window",
            class_name=self.class_name
        )
        child_window = self.init_plain_window(self.parent_window)

        # Initialise the window
        self.const.pdebug(
            "Initialising the window's meta data",
            class_name=self.class_name
        )
        self.init_window(
            child_window,
            title="MDI viewer",
            bkg="white",
            width=self.width + self.x_offset,
            height=self.height + self.y_offset+object_height,
            position_x=window_coord[0],
            position_y=window_coord[1],
            fullscreen=False,
            resizable=True
        )

        # Add a frame for the title
        self.const.pdebug(
            "Adding a frame for the title",
            class_name=self.class_name
        )
        title_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="blue" if self.debug else self.bg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )

        # Add a frame for the image
        self.const.pdebug(
            "Adding a frame for the image",
            class_name=self.class_name
        )
        image_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="orange" if self.debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )

        # Add a frame for the footer
        self.const.pdebug(
            "Adding a frame for the footer",
            class_name=self.class_name
        )
        footer_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="cyan" if self.debug else self.bg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.BOTTOM,
            fill=tk.X,
            anchor=tk.CENTER
        )

        # Add a frame for the buttons
        self.const.pdebug(
            "Adding a frame for the buttons",
            class_name=self.class_name
        )
        button_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="purple" if self.debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.BOTTOM,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a frame for the previous button
        self.const.pdebug(
            "Adding a frame for the previous button",
            class_name=self.class_name
        )
        button_prev_frame = self.add_frame(
            button_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="green" if self.debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a frame for the viewing area
        self.const.pdebug(
            "Adding a frame for the viewing area",
            class_name=self.class_name
        )
        image_viewer_frame = self.add_frame(
            image_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="yellow" if self.debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a frame for the buttons
        self.const.pdebug(
            "Adding a frame for the buttons",
            class_name=self.class_name
        )
        button_next_frame = self.add_frame(
            button_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="red" if self.debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a label to display the title of the window
        self.const.pdebug(
            "Adding a label to display the title of the window",
            class_name=self.class_name
        )
        self.title_label = self.add_label(
            title_frame,
            text="MDI Viewer",
            bkg=self.bg,
            fg=self.fg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )

        # Add a label to display the title of the image
        self.const.pdebug(
            "Adding a label to display the title of the image",
            class_name=self.class_name
        )
        self.image_viewer = self.add_label(
            image_viewer_frame,
            text="",
            bkg=self.bg,
            fg=self.fg,
            width=width,
            height=height - self.y_offset,
            position_x=20,
            position_y=0,
            side=tk.TOP,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a section to display an error if present
        self.const.pdebug(
            "Adding a section to display an error if present",
            class_name=self.class_name
        )
        self.image_viewer_error = self.add_label(
            image_viewer_frame,
            text="",
            bkg=self.bg,
            fg=self.fg,
            width=width,
            height=2,
            position_x=20,
            position_y=0,
            side=tk.TOP,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        # Add a button to show the previous image
        self.const.pdebug(
            "Adding a button to show the previous image",
            class_name=self.class_name
        )
        self.button_prev = self.add_button(
            button_prev_frame,
            text="Previous",
            fg=self.fg,
            bkg=self.bg,
            side=tk.TOP,
            command=self._previous_image,
            width=button_width,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )

        # Add a button to show the next image
        self.const.pdebug(
            "Adding a button to show the next image",
            class_name=self.class_name
        )
        self.button_next = self.add_button(
            button_next_frame,
            text="Next",
            fg=self.fg,
            bkg=self.bg,
            side=tk.LEFT,
            command=self._next_image,
            width=button_width,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )

        # Add the button to view the image in the system viewer
        self.const.pdebug(
            "Adding the button to view the image in the system viewer",
            class_name=self.class_name
        )
        self.button_open_in_viewer = self.add_button(
            button_next_frame,
            text="Open in system viewer",
            fg=self.fg,
            bkg=self.bg,
            side=tk.LEFT,
            command=self._open_in_system_viewer,
            width=button_width*2,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )

        # Add the image count
        self.const.pdebug(
            "Adding the image count",
            class_name=self.class_name
        )
        self.image_count = self.add_label(
            footer_frame,
            text=f"Image {self.current_image + 1}/{self.max_images + 1}",
            bkg=self.bg,
            fg=self.fg,
            width=self.width - (button_width*2),
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )

        # Add watermark to the window
        self.const.pdebug(
            "Adding watermark to the window",
            class_name=self.class_name
        )
        self.add_watermark(
            window=footer_frame,
            side=tk.RIGHT,
            anchor=tk.E,
            bkg=self.bg,
            fg=self.fg
        )

        # Change the images
        self.const.pdebug(
            "setting the images",
            class_name=self.class_name
        )
        self._previous_image()
        self._next_image()
        self.const.pdebug(
            "Updating the current image",
            class_name=self.class_name
        )
        child_window.wait_window()
        return True


if __name__ == "__main__":
    ERROR = 1
    SUCCESS = 0
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 400
    DEBUG = True
    DELAY_INIT = False
    if (len(sys.argv) == 2 and sys.argv[1] in ("--help", "--h", "--?", "-h", "-?", "-help", "/?", "/h", "/help")):
        print(f"Usage: python3 {sys.argv[0]} <image_directory_path>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <image_directory_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if os.path.isdir(sys.argv[1]) is False:
        image_path = "../../sample_images"
        print(
            f"Error: '{sys.argv[1]}' is not a directory, defaulting to: {image_path}"
        )
        if os.path.isdir(image_path) is False:
            print(f"Error: default path '{image_path}' is not a directory")
            sys.exit(1)
    VII = ViewImage(
        None,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        success=SUCCESS,
        error=ERROR,
        parent_const=None,
        debug=DEBUG,
        delay_init=DELAY_INIT
    )
    ressources = []
    if os.path.exists(image_path) is True:
        images = os.listdir(image_path)
        for index, item in enumerate(images):
            ressources.append(os.path.join(image_path, item))
        ressources.append("Not a path")
    VII.view(
        ressources,
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
