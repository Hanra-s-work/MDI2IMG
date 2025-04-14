"""
    File in charge of testing the library via functional tests.
"""
import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

SUCCESS = 0
ERROR = 1
GLOBAL_STATUS = SUCCESS


def update_global_status(status):
    """_summary_

    Args:
        status (_type_): _description_
    """
    global GLOBAL_STATUS
    if status != SUCCESS:
        GLOBAL_STATUS = ERROR


def check_and_create_directories(*paths):
    """_summary_

    Returns:
        _type_: _description_
    """
    for path in paths:
        if not os.path.isdir(path):
            print(f"Creating missing directory: {path}")
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                print(f"Error: Cannot create directory '{path}': {e}")
                return ERROR
    return SUCCESS


def copy_file(source: str, dest: str, force: bool = True) -> int:
    """_summary_

    Args:
        source (str): _description_
        dest (str): _description_
    """
    if os.path.exists(dest) and force and os.path.isfile(dest):
        os.remove(dest)
    try:
        shutil.copy(source, dest, follow_symlinks=False)
    except Exception as e:
        print(f"Error copying file: {e}")
        return ERROR
    return SUCCESS


def copy_test_images(source: str, destination: str):
    """_summary_

    Args:
        source (Path): _description_
        destination (Path): _description_

    Returns:
        _type_: _description_
    """
    try:
        for file in os.listdir(source):
            if file in (".", "..") or os.path.islink(file) or os.path.isdir(file):
                continue
            shutil.copy(
                os.path.join(source, file),
                destination,
                follow_symlinks=False
            )
        return SUCCESS
    except Exception as e:
        print(f"Error copying test images: {e}")
        return ERROR


def run_program(bin_cmd: str, input_file: str, *extra_args):
    """_summary_

    Args:
        bin_cmd (_type_): _description_
        input_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not os.path.exists(input_file):
        print(f"Input file does not exist: {input_file}")
        return ERROR

    command = [*bin_cmd.split(), input_file, *extra_args]
    print("Running command:", " ".join(command))
    status = subprocess.call(command)
    update_global_status(status)

    print("Command status: ", end="")
    if status != SUCCESS:
        print(f"[KO] Command failed with code: {status}")
    else:
        print("[OK]")
    return status


def recreate_in_virtual_env(venv_dir):
    """_summary_

    Args:
        venv_dir (_type_): _description_
    """
    print("Re-invoking script inside the virtual environment...")
    python_bin: str = (
        f"{Path(venv_dir)}/Scripts/python.exe"
        if platform.system() == "Windows"
        else f"{Path(venv_dir)}/bin/python"
    )

    if not os.path.exists(python_bin):
        print(f"Error: Could not find Python in venv at {python_bin}")
        sys.exit(ERROR)

    os.execv(str(python_bin), [str(python_bin), *sys.argv])


def ensure_virtual_env(env_name):
    """_summary_

    Args:
        env_name (_type_): _description_
    """
    if "VIRTUAL_ENV" not in os.environ:
        venv_path = Path(env_name)
        if not venv_path.exists():
            print(f"Creating virtual environment: {env_name}")
            subprocess.check_call([sys.executable, "-m", "venv", env_name])

        recreate_in_virtual_env(env_name)
    else:
        print("Virtual environment is already active.")


def install_dependencies():
    """_summary_
    """
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    subprocess.check_call(["pip", "install", "-r", "requirements.dev.txt"])


def build_and_install_library():
    """_summary_
    """
    print("Building the library...")
    subprocess.check_call(["python", "-m", "build"])

    print("Installing the built library...")
    dist_files = list(Path("dist").glob("mdi2img-*.tar.gz"))
    if not dist_files:
        print("Error: No distribution file found in ./dist.")
        sys.exit(ERROR)

    subprocess.check_call(["pip", "install", "--upgrade", str(dist_files[0])])


def run_functional_tests(mdi_folder: str, dest_folder: str, base_folder: str):
    """_summary_

    Args:
        mdi_folder (_type_): _description_
        dest_folder (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Running functional tests...")

    def get_correct_runner_type(raw_library: bool = True):
        """_summary_

        Args:
            raw_library (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if raw_library:
            if platform.system() == "Windows":
                return f"{sys.executable} mdi2img"
            return f"{sys.executable} ./mdi2img"
        else:
            return f"{sys.executable} -m mdi2img"

    def destination_arg(dest_path):
        """_summary_

        Args:
            dest_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        return f"--destination=\"{dest_path}\""

    def format_arg(format_type: str = "png"):
        """_summary_

        Args:
            format_type (str, optional): _description_. Defaults to "png".

        Returns:
            _type_: _description_
        """
        return f"--format='{format_type}'"

    base_arg_debug = '--debug'

    # Start testing

    print("Running the tests...")
    print("Tesing the raw version of the library...")
    # Testing an mdi to png conversion with a specified format and destination
    run_program(
        get_correct_runner_type(True),
        os.path.join(mdi_folder, "C_futoshi_stand.mdi"),
        destination_arg(os.path.join(dest_folder, "C_futoshi_stand.png")),
        format_arg("png")
    )
    # Testing an mdi to png conversion with a specified format, destination and debug
    run_program(
        get_correct_runner_type(True),
        os.path.join(mdi_folder, "C_goro_stand.mdi"),
        base_arg_debug,
        destination_arg(os.path.join(dest_folder, "C_goro_stand.png")),
        format_arg("png")
    )
    # Testing an mdi to png conversion with a specified destination
    run_program(
        get_correct_runner_type(True),
        os.path.join(mdi_folder, "C_hiro_stand.mdi"),
        destination_arg(os.path.join(dest_folder, "C_hiro_stand.png"))
    )
    # Testing an mdi to png conversion with a specified destination and debug
    run_program(
        get_correct_runner_type(True),
        os.path.join(mdi_folder, "C_ichigo_stand.mdi"),
        destination_arg(os.path.join(dest_folder, "C_ichigo_stand.png")),
        base_arg_debug
    )
    # Testing file conversion without a destination
    copy_file(
        os.path.join(mdi_folder, "C_ikuno_stand.mdi"),
        os.path.join(dest_folder, "C_ikuno_stand.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(True),
        os.path.join(dest_folder, "C_ikuno_stand.mdi")
    )
    # Testing file conversion without a destination and debug
    copy_file(
        os.path.join(mdi_folder, "C_kokoro_stand.mdi"),
        os.path.join(dest_folder, "C_kokoro_stand.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(True),
        os.path.join(dest_folder, "C_kokoro_stand.mdi"),
        base_arg_debug
    )
    # Testing file conversion with a specified format
    copy_file(
        os.path.join(mdi_folder, "C_miku_stand.mdi"),
        os.path.join(dest_folder, "C_miku_stand.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(True),
        os.path.join(dest_folder, "C_miku_stand.mdi"),
        format_arg("png")
    )
    # Testing file conversion with a specified format and debug
    copy_file(
        os.path.join(mdi_folder, "C_mitsuru_stand.mdi"),
        os.path.join(dest_folder, "C_mitsuru_stand.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(True),
        os.path.join(dest_folder, "C_mitsuru_stand.mdi"),
        base_arg_debug,
        format_arg("png")
    )
    # Raw library with folder, destination and format
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_DESTINATION_FORMAT")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(True),
        mdi_folder,
        destination_arg(tmp_folder),
        format_arg("png")
    )
    # Raw library with debug argument, folder, destination and format
    tmp_folder = os.path.join(
        base_folder,
        "RAW_FOLDER_DESTINATION_FORMAT_DEBUG"
    )
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(True),
        mdi_folder,
        destination_arg(tmp_folder),
        format_arg("png"),
        base_arg_debug
    )
    # Raw library with folder and destination
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_DESTINATION")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(True),
        mdi_folder,
        destination_arg(tmp_folder)
    )
    # Raw library with debug argument, folder and destination
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_DESTINATION_DEBUG")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(True),
        mdi_folder,
        destination_arg(tmp_folder),
        base_arg_debug
    )
    # Raw library with folder
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER")
    check_and_create_directories(
        tmp_folder
    )
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(True), tmp_folder)
    # Raw library with debug argument and folder
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_DEBUG")
    check_and_create_directories(
        tmp_folder
    )
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(True), tmp_folder, base_arg_debug)
    # Raw library with folder and format
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_FORMAT")
    check_and_create_directories(tmp_folder)
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(True), tmp_folder, format_arg("png"))
    # Raw library with debug argument, folder and format
    tmp_folder = os.path.join(base_folder, "RAW_FOLDER_DEBUG_FORMAT")
    check_and_create_directories(tmp_folder)
    copy_test_images(mdi_folder, tmp_folder)
    run_program(
        get_correct_runner_type(True),
        tmp_folder,
        base_arg_debug,
        format_arg("png")
    )
    print("Testing the compiled version of the library...")
    # Testing an mdi to png conversion with a specified format and destination
    run_program(
        get_correct_runner_type(False),
        os.path.join(mdi_folder, "C_zero_two_stand.mdi"),
        destination_arg(os.path.join(dest_folder, "C_zero_two_stand.png")),
        format_arg("png")
    )
    # Testing an mdi to png conversion with a specified format, destination and debug
    run_program(
        get_correct_runner_type(False),
        os.path.join(mdi_folder, "C_zorome_stand.mdi"),
        base_arg_debug,
        destination_arg(os.path.join(dest_folder, "C_zorome_stand.png")),
        format_arg("png")
    )
    # Testing an mdi to png conversion with a specified destination
    run_program(
        get_correct_runner_type(False),
        os.path.join(mdi_folder, "9_s_Model_Franxx.mdi"),
        destination_arg(os.path.join(dest_folder, "9_s_Model_Franxx.png"))
    )
    # Testing an mdi to png conversion with a specified destination and debug
    run_program(
        get_correct_runner_type(False),
        os.path.join(mdi_folder, "C_argentea.mdi"),
        destination_arg(os.path.join(dest_folder, "C_argentea.png")),
        base_arg_debug
    )
    # Testing file conversion without a destination
    copy_file(
        os.path.join(mdi_folder, "C_chlorophytum.mdi"),
        os.path.join(dest_folder, "C_chlorophytum.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(False),
        os.path.join(dest_folder, "C_chlorophytum.mdi")
    )
    # Testing file conversion without a destination and debug
    copy_file(
        os.path.join(mdi_folder, "C_delphinium.mdi"),
        os.path.join(dest_folder, "C_delphinium.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(False),
        os.path.join(dest_folder, "C_delphinium.mdi"),
        base_arg_debug
    )
    # Testing file conversion with a specified format
    copy_file(
        os.path.join(mdi_folder, "C_genista.mdi"),
        os.path.join(dest_folder, "C_genista.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(False),
        os.path.join(dest_folder, "C_genista.mdi"),
        format_arg("png")
    )
    # Testing file conversion with a specified format and debug
    copy_file(
        os.path.join(mdi_folder, "C_strelizia.mdi"),
        os.path.join(dest_folder, "C_strelizia.mdi"),
        force=True
    )
    run_program(
        get_correct_runner_type(False),
        os.path.join(dest_folder, "C_strelizia.mdi"),
        base_arg_debug,
        format_arg("png")
    )
    # module library with folder, destination and format
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_DESTINATION_FORMAT")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(False),
        mdi_folder,
        destination_arg(tmp_folder),
        format_arg("png")
    )
    # module library with debug argument, folder, destination and format
    tmp_folder = os.path.join(
        base_folder,
        "MODULE_FOLDER_DESTINATION_FORMAT_DEBUG"
    )
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(False),
        mdi_folder,
        destination_arg(tmp_folder),
        format_arg("png"),
        base_arg_debug
    )
    # module library with folder and destination
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_DESTINATION")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(False),
        mdi_folder,
        destination_arg(tmp_folder)
    )
    # module library with debug argument, folder and destination
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_DESTINATION_DEBUG")
    check_and_create_directories(tmp_folder)
    run_program(
        get_correct_runner_type(False),
        mdi_folder,
        destination_arg(tmp_folder),
        base_arg_debug
    )
    # module library with folder
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER")
    check_and_create_directories(
        tmp_folder
    )
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(False), tmp_folder)
    # module library with debug argument and folder
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_DEBUG")
    check_and_create_directories(
        tmp_folder
    )
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(False), tmp_folder, base_arg_debug)
    # module library with folder and format
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_FORMAT")
    check_and_create_directories(tmp_folder)
    copy_test_images(mdi_folder, tmp_folder)
    run_program(get_correct_runner_type(False), tmp_folder, format_arg("png"))
    # module library with debug argument, folder and format
    tmp_folder = os.path.join(base_folder, "MODULE_FOLDER_DEBUG_FORMAT")
    check_and_create_directories(tmp_folder)
    copy_test_images(mdi_folder, tmp_folder)
    run_program(
        get_correct_runner_type(False),
        tmp_folder,
        base_arg_debug,
        format_arg("png")
    )
    print("Testing completed.")


def clean_up(folder: Path):
    """_summary_

    Args:
        folder (Path): _description_
    """
    print("Cleaning up test directory...")
    try:
        shutil.rmtree(folder)
        print("Cleanup complete.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
    sys.exit(ERROR)


def main():
    """
    Main function to run the testing script.
    """
    base_folder = os.path.join(Path.cwd(), "test_image_zone")
    env_name = os.path.join(Path.cwd(), "test_env")
    ensure_virtual_env(env_name)

    mdi_folder = os.path.join(base_folder, "mdi")
    dest_folder = os.path.join(base_folder, "destination")
    source_images = os.path.join(Path.cwd(), "sample_images", "mdi")

    if check_and_create_directories(base_folder, mdi_folder, dest_folder) != SUCCESS:
        sys.exit(ERROR)

    if copy_test_images(source_images, mdi_folder) != SUCCESS:
        sys.exit(ERROR)

    install_dependencies()
    build_and_install_library()
    run_functional_tests(mdi_folder, dest_folder, base_folder)
    clean_up(Path(base_folder))

    if "VIRTUAL_ENV" not in os.environ and os.path.exists(env_name):
        remove_virtual_env = input(
            "Do you want to remove the virtual environment? (y/n): ")
        if remove_virtual_env.lower() == "y":
            shutil.rmtree(env_name)
            print(f"Virtual environment '{env_name}' removed.")
        else:
            print(f"Virtual environment '{env_name}' not removed.")
    print("Testing completed.")
    sys.exit(GLOBAL_STATUS)


if __name__ == "__main__":
    main()
