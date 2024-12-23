"""_summary_
    This is the file that is in charge of changing the default output format of the converter to one that is desired by the user.
"""

from typing import Union, List

from PIL import Image

from display_tty import Disp
from .constants import Constants, ERROR, SUCCESS

AVAILABLE_FORMATS_HELP = {
    "png": "Portable Network Graphics is a lossless format that supports transparency. APNG (Animated PNG) is an extension supporting simple animations.",
    # "jpg": "The most common image format, using lossy compression to reduce file size. Widely used for web photographs. Extensions: `.jpg`, `.jpeg`, `.jfif`, `.jpe`.",
    "jpeg": "The most common image format, using lossy compression to reduce file size. Widely used for web photographs. Extensions: `.jpg`, `.jpeg`, `.jfif`, `.jpe`.",
    "gif": "Graphics Interchange Format, limited to 256 colors. Supports animation, but images may not appear animated here.",
    "tiff": "Tagged Image File Format, commonly used in professional photography and desktop publishing. Supports lossless compression, layers, and multiple pages.",
    "bmp": "Bitmap Image File is a standard image format on Windows. It stores color data for each pixel in the image without compression, leading to large file sizes.",
    "webp": "A modern image format that provides both lossy and lossless compression. Optimized for the web, offering smaller file sizes with high quality.",
    "pdf": "Portable Document Format, mainly used for documents but can include embedded images. Pillow can generate and read images within PDFs.",
    "psd": "Adobe Photoshop Document format, used to store images with layers, channels, and various adjustments.",
    "eps": "Encapsulated PostScript and PostScript formats are used for vector graphics and layouts. Popular in desktop publishing. Extensions: `.eps`, `.ps`.",
    "ico": "Icon file format used in Windows for storing multiple sizes and color depths of icons for applications and shortcuts.",
    "icns": "Apple Icon Image format used on macOS for application icons. Supports multiple resolutions and color depths.",
    "apng": "Portable Network Graphics is a lossless format that supports transparency. APNG (Animated PNG) is an extension supporting simple animations.",
    "jfif": "The most common image format, using lossy compression to reduce file size. Widely used for web photographs. Extensions: `.jpg`, `.jpeg`, `.jfif`, `.jpe`.",
    "mpg": "A video format, but Pillow can process individual frames of MPEG videos. Extensions: `.mpg`, `.mpeg`.",
    "mpeg": "A video format, but Pillow can process individual frames of MPEG videos. Extensions: `.mpg`, `.mpeg`.",
    "tif": "Tagged Image File Format, commonly used in professional photography and desktop publishing. Supports lossless compression, layers, and multiple pages.",
    "msp": "Microsoft Paint bitmap image file, an old format used by early versions of MS Paint.",
    "pbm": "A family of simple uncompressed image formats (Portable Pixmap, Portable Graymap, Portable Bitmap) used for basic image storage. Extensions: `.pbm`, `.pgm`, `.ppm`, `.pnm`, `.pfm`.",
    "pgm": "A family of simple uncompressed image formats (Portable Pixmap, Portable Graymap, Portable Bitmap) used for basic image storage. Extensions: `.pbm`, `.pgm`, `.ppm`, `.pnm`, `.pfm`.",
    "ppm": "A family of simple uncompressed image formats (Portable Pixmap, Portable Graymap, Portable Bitmap) used for basic image storage. Extensions: `.pbm`, `.pgm`, `.ppm`, `.pnm`, `.pfm`.",
    "pnm": "A family of simple uncompressed image formats (Portable Pixmap, Portable Graymap, Portable Bitmap) used for basic image storage. Extensions: `.pbm`, `.pgm`, `.ppm`, `.pnm`, `.pfm`.",
    "pfm": "A family of simple uncompressed image formats (Portable Pixmap, Portable Graymap, Portable Bitmap) used for basic image storage. Extensions: `.pbm`, `.pgm`, `.ppm`, `.pnm`, `.pfm`.",
    "blp": "Used primarily in Blizzard Entertainment games, such as World of Warcraft. It's a compressed format similar to JPEG, but optimized for fast decompression in games.",
    "dib": "Bitmap Image File is a standard image format on Windows. It stores color data for each pixel in the image without compression, leading to large file sizes.",
    "bufr": "Binary Universal Form for the Representation of meteorological data. Used in meteorology to store and exchange weather-related information.",
    "cur": "Cursor file format, used to define the image of a mouse pointer on Windows.",
    "pcx": "One of the earliest image formats for PC Paintbrush software. It's a simple bitmap image format, while DCX is an extension supporting multiple pages.",
    "dcx": "One of the earliest image formats for PC Paintbrush software. It's a simple bitmap image format, while DCX is an extension supporting multiple pages.",
    "dds": "DirectDraw Surface format, commonly used for storing textures and mipmaps in video games.",
    "fit": "Flexible Image Transport System, mainly used in astronomy for storing scientific images with associated metadata. Extensions: `.fit`, `.fits`.",
    "fits": "Flexible Image Transport System, mainly used in astronomy for storing scientific images with associated metadata. Extensions: `.fit`, `.fits`.",
    "fli": "Animation formats developed by Autodesk. FLI and FLC files are used for storing simple animations in older software. Extensions: `.fli`, `.flc`.",
    "flc": "Animation formats developed by Autodesk. FLI and FLC files are used for storing simple animations in older software. Extensions: `.fli`, `.flc`.",
    "ftc": "Format for storing texture data in video games, particularly on the PlayStation 2. Extensions: `.ftc`, `.ftu`.",
    "ftu": "Format for storing texture data in video games, particularly on the PlayStation 2. Extensions: `.ftc`, `.ftu`.",
    "gbr": "GIMP Brush file used by the GNU Image Manipulation Program (GIMP) to store custom brush shapes.",
    "grib": "GRIdded Binary, a concise data format used in meteorology to store weather forecast data.",
    "h5": "Hierarchical Data Format version 5, used for storing large amounts of scientific data. Extensions: `.h5`, `.hdf`.",
    "hdf": "Hierarchical Data Format version 5, used for storing large amounts of scientific data. Extensions: `.h5`, `.hdf`.",
    "jp2": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "j2k": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "jpc": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "jpf": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "jpx": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "j2c": "An improved version of JPEG, offering better compression and quality, as well as support for lossless compression and alpha channels. Extensions: `.jp2`, `.j2k`, `.jpc`, `.jpf`, `.jpx`, `.j2c`.",
    "im": "An internal format used by the PIL library to store images.",
    "iim": "Used for storing metadata in images, typically in news photography to include information like captions and authorship.",
    "mpo": "Multi-Picture Object format, used for storing multiple images in a single file, often for 3D images from digital cameras.",
    "palm": "Image format used by Palm OS devices, with limited color support and simple compression.",
    "pcd": "Kodak Photo CD format, used for storing high-resolution images scanned from film.",
    "pxr": "Used by Pixar for raster images, particularly in the RenderMan software.",
    "qoi": "Quite OK Image, a new image format designed to be simple, fast, and efficient, without sacrificing quality.",
    "bw": "Silicon Graphics Image format, used primarily on Silicon Graphics workstations. Extensions: `.bw`, `.rgb`, `.rgba`, `.sgi`.",
    "rgb": "Silicon Graphics Image format, used primarily on Silicon Graphics workstations. Extensions: `.bw`, `.rgb`, `.rgba`, `.sgi`.",
    "rgba": "Silicon Graphics Image format, used primarily on Silicon Graphics workstations. Extensions: `.bw`, `.rgb`, `.rgba`, `.sgi`.",
    "sgi": "Silicon Graphics Image format, used primarily on Silicon Graphics workstations. Extensions: `.bw`, `.rgb`, `.rgba`, `.sgi`.",
    "ras": "Sun Raster format, used on Sun Microsystems workstations.",
    "tga": "Targa format, originally developed by Truevision, commonly used in video game graphics and simple image storage. Extensions: `.tga`, `.icb`, `.vda`, `.vst`.",
    "icb": "Targa format, originally developed by Truevision, commonly used in video game graphics and simple image storage. Extensions: `.tga`, `.icb`, `.vda`, `.vst`.",
    "vda": "Targa format, originally developed by Truevision, commonly used in video game graphics and simple image storage. Extensions: `.tga`, `.icb`, `.vda`, `.vst`.",
    "vst": "Targa format, originally developed by Truevision, commonly used in video game graphics and simple image storage. Extensions: `.tga`, `.icb`, `.vda`, `.vst`.",
    "wmf": "Windows Metafile and Enhanced Metafile formats, used for storing vector and bitmap data on Windows systems. Extensions: `.wmf`, `.emf`.",
    "emf": "Windows Metafile and Enhanced Metafile formats, used for storing vector and bitmap data on Windows systems. Extensions: `.wmf`, `.emf`.",
    "xbm": "X Bitmap format, used for storing monochrome icons and cursors in the X Window System.",
    "xpm": "X PixMap format, similar to XBM, but supports color. It's used for simple graphics in the X Window System."
}


AVAILABLE_FORMATS = list(AVAILABLE_FORMATS_HELP)


class ChangeImageFormat:
    """_summary_
    The class in charge of orchestrating the image formats.
    """

    def __init__(self, constants: Constants, success: int = SUCCESS, error: int = ERROR) -> None:
        self.success = success
        self.error = error
        self.const: Constants = constants
        self.disp: Disp = self.const.dttyi

    def _check_output_file(self, output_file: str, img_format: str) -> Union[str, List[str]]:
        """_summary_
            This is a function that will analyse the name of the output file and return the path and temporary path (if output format is not tiff)

        Args:
            output_file (str): _description_
            img_format (str): _description_

        Returns:
            Union[str, List[str,str]: _description_: A list is returned with the paths of the output files if a second conversion step is required. Otherwise, only the final path is returned.
        """
        img_format = img_format.lower()
        # Get the extension of the file
        output_file_format = output_file.split(".")[-1].lower()
        # Get the name of the file
        output_file_name = output_file.replace("\\", "/").split("/")[-1]
        output_file_name = output_file_name.split(".")
        output_file_name.pop(-1)
        output_file_name = ".".join(output_file_name)
        # Get the path of the file
        output_file_path = output_file.replace("\\", "/").split("/")
        output_file_path.pop(-1)
        output_file_path = "/".join(output_file_path)

        if output_file_format != img_format:
            warning_msg = "The output format and the format in the file name do not match! "
            warning_msg += "The program will default to the first available format of the two."
            self.const.pwarning(warning_msg)
            if output_file_format in AVAILABLE_FORMATS:
                img_format = output_file_format
            else:
                output_file_format = img_format
            self.const.pinfo(f"The format is now {img_format}")
        if img_format != "tiff" and output_file_format != "tiff":
            temp_export = f"{self.const.temporary_img_folder}/"
            temp_export += f"{output_file_name}.tiff"
            final_export = f"{output_file_path}/"
            final_export += f"{output_file_name}.{img_format}"
            return [temp_export, final_export]
        return output_file

    def _get_new_name(self, image: str = "", img_format: str = "") -> str:
        """_summary_
        Create a new name for the destination image based on the input.

        Args:
            image (str, optional): _description_. Defaults to "".
            format (str, optional): _description_. Defaults to "".

        Returns:
            str: _description_
        """
        dest = image.split(".")
        dest.pop(-1)
        dest.append(img_format.lower())
        dest = ".".join(dest)
        return dest

    def to_desired_format(self, image: str = "", output_name: str = "", img_format: str = "png") -> int:
        """_summary_
        Convert an image to tiff format

        Args:
            image (str, optional): _description_: The image to convert. Defaults to "".

        Returns:
            int: _description_: The status of the convertion (success:int  or error:int)
        """
        if image == "":
            self.const.pcritical("No image provided!")
            return self.error
        if output_name == "":
            self.const.pwarning(
                "Not destination name was provided, generating one."
            )
            output_name = self._get_new_name(image, img_format)
            self.const.pinfo(f"The destination name is '{output_name}'\n")
        try:
            img = Image.open(image)
            img.save(output_name, format=img_format)
            return self.success
        except Exception as e:
            self.const.perror(f"Failed to convert image:\nError: '{e}'")
            return self.error
