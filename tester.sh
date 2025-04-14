#!/bin/bash

ERROR=1
SUCCESS=0
GLOBAL_STATUS=$SUCCESS

function update_global_status {
    if [ $1 -ne $SUCCESS ]; then
        GLOBAL_STATUS=$ERROR
    fi
}

function check_destination {
    for arg in "$@"; do
        if [ ! -d "$arg" ]; then
            echo "Destination folder '$arg' does not exists. creating it."
            mkdir -p "$arg"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to create destination folder '$arg'."
                return $ERROR
            fi
        fi
    done
}

function run_program {
    local bin=${1:-"python -m mdi2img"}
    local input_file="$2"
    if [ ! -f "$input_file" ]; then
        echo "Error: Input file '$input_file' does not exist."
        return $ERROR
    fi
    shift 2
    local extra_args="$@"
    local command="$bin $input_file $extra_args"
    echo "Running command: $command"
    eval $command
    STATUS=$?
    update_global_status $STATUS
    echo -n "Command execution status: "
    if [ $STATUS -ne 0 ]; then
        echo "[KO]"
        echo "Error: Command failed with code: $STATUS."
        return $STATUS
    fi
    echo "[OK]"
}

# Creating the test zone folder
echo "Ctreating the test zone folder..."
BASE_FOLDER="$(pwd)/test_image_zone"
BASE_FOLDER_MDI="$BASE_FOLDER/mdi"
BASE_FOLDER_DESTINATION="$BASE_FOLDER/destination"

check_destination $BASE_FOLDER $BASE_FOLDER_MDI $BASE_FOLDER_DESTINATION
if [ $? -ne 0 ]; then
    exit $ERROR
fi
echo "Test zone folders created."

# Copying the test images
echo "Copying the test images..."
cp -rvf "$(pwd)/sample_images/mdi/"* $BASE_FOLDER/mdi
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy test images."
    exit $ERROR
fi
echo "Test images copied."

# activate the environment
ENV_NAME="lenv"
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating the virtual environment '$ENV_NAME'..."
    . "$ENV_NAME/bin/activate"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate the virtual environment '$ENV_NAME'."
        exit $ERROR
    fi
else
    echo "Virtual environment already activated."
fi

# Install the dependencies
echo "Installing the dependencies (if not already present)..."
pip install -r requirements.txt
pip install -r requirements.dev.txt

# Compile the library
echo "Compiling the library..."
python3 -m build

# Install the library
echo "Installing the library..."
pip install --upgrade dist/mdi2img-*.tar.gz
if [ $? -ne 0 ]; then
    echo "Error: Failed to install the library."
    exit $ERROR
fi

# Paths to the compiled and not compiled versions of the library
RUN_RAW_LIBRARY="python3 ./mdi2img"
RUN_COMPILED_LIBRARY="python3 -m mdi2img"

# default settings (variables)
BASE_ARG_DEBUG="--debug"
BASE_ARG_FORMAT="--format=\"png\""
BASE_ARG_DESTINATION="--destination=\"$BASE_FOLDER_DESTINATION\""

# Run the tests
echo "Running the tests..."
echo "Tesing the raw version of the library..."
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI/C_futoshi_stand.mdi" "$BASE_ARG_DESTINATION/C_futoshi_stand.png" $BASE_ARG_FORMAT
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI/C_goro_stand.mdi" $BASE_ARG_DEBUG "$BASE_ARG_DESTINATION/C_goro_stand.png" $BASE_ARG_FORMAT
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI/C_hiro_stand.mdi" "$BASE_ARG_DESTINATION/C_hiro_stand.png"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI/C_ichigo_stand.mdi" $BASE_ARG_DEBUG "$BASE_ARG_DESTINATION/C_ichigo_stand.png"
cp -f "$BASE_FOLDER_MDI/C_ikuno_stand.mdi" "$BASE_FOLDER_DESTINATION/C_ikuno_stand.mdi"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_DESTINATION/C_ikuno_stand.mdi"
cp -f "$BASE_FOLDER_MDI/C_kokoro_stand.mdi" "$BASE_FOLDER_DESTINATION/C_kokoro_stand.mdi"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_DESTINATION/C_kokoro_stand.mdi" $BASE_ARG_DEBUG
cp -f "$BASE_FOLDER_MDI/C_miku_stand.mdi" "$BASE_FOLDER_DESTINATION/C_miku_stand.mdi"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_DESTINATION/C_miku_stand.mdi" $BASE_ARG_FORMAT
cp -f "$BASE_FOLDER_MDI/C_mitsuru_stand.mdi" "$BASE_FOLDER_DESTINATION/C_mitsuru_stand.mdi"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_DESTINATION/C_mitsuru_stand.mdi" $BASE_ARG_DEBUG $BASE_ARG_FORMAT
# Raw library with folder, destination and format
check_destination "$BASE_FOLDER/RAW_FOLDER_DESTINATION_FORMAT"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/RAW_FOLDER_DESTINATION_FORMAT" $BASE_ARG_FORMAT
# Raw library with debug argument, folder, destination and format
check_destination "$BASE_FOLDER/RAW_FOLDER_DESTINATION_FORMAT_DEBUG"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/RAW_FOLDER_DESTINATION_FORMAT_DEBUG" $BASE_ARG_FORMAT $BASE_ARG_DEBUG
# Raw library with folder and destination
check_destination "$BASE_FOLDER/RAW_FOLDER_DESTINATION"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/RAW_FOLDER_DESTINATION"
# Raw library with debug argument, folder and destination
check_destination "$BASE_FOLDER/RAW_FOLDER_DESTINATION_DEBUG"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/RAW_FOLDER_DESTINATION_DEBUG" $BASE_ARG_DEBUG
# Raw library with folder
check_destination "$BASE_FOLDER/RAW_FOLDER"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/RAW_FOLDER"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER/RAW_FOLDER"
# Raw library with debug argument and folder
check_destination "$BASE_FOLDER/RAW_FOLDER_DEBUG"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/RAW_FOLDER_DEBUG"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER/RAW_FOLDER_DEBUG" $BASE_ARG_DEBUG
# Raw library with folder and format
check_destination "$BASE_FOLDER/RAW_FOLDER_FORMAT"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/RAW_FOLDER_FORMAT"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER/RAW_FOLDER_FORMAT" $BASE_ARG_FORMAT
# Raw library with debug argument, folder and format
check_destination "$BASE_FOLDER/RAW_FOLDER_DEBUG_FORMAT"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/RAW_FOLDER_DEBUG_FORMAT"
run_program $RUN_RAW_LIBRARY "$BASE_FOLDER/RAW_FOLDER_DEBUG_FORMAT" $BASE_ARG_DEBUG $BASE_ARG_FORMAT
echo "Testing the compiled version of the library..."
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_MDI/C_zero_two_stand.mdi" "$BASE_ARG_DESTINATION/C_zero_two_stand.png" $BASE_ARG_FORMAT
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_MDI/C_zorome_stand.mdi" $BASE_ARG_DEBUG "$BASE_ARG_DESTINATION/C_zorome_stand.png" $BASE_ARG_FORMAT
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_MDI/9_s_Model_Franxx.mdi" "$BASE_ARG_DESTINATION/9_s_Model_Franxx.png"
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_MDI/C_argentea.mdi" $BASE_ARG_DEBUG "$BASE_ARG_DESTINATION/C_argentea.png"
cp -f "$BASE_FOLDER_MDI/C_chlorophytum.mdi" "$BASE_FOLDER_DESTINATION/C_chlorophytum.mdi"
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_DESTINATION/C_chlorophytum.mdi"
cp -f "$BASE_FOLDER_MDI/C_delphinium.mdi" "$BASE_FOLDER_DESTINATION/C_delphinium.mdi"
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_DESTINATION/C_delphinium.mdi" $BASE_ARG_DEBUG
cp -f "$BASE_FOLDER_MDI/C_genista.mdi" "$BASE_FOLDER_DESTINATION/C_genista.mdi"
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_DESTINATION/C_genista.mdi" $BASE_ARG_FORMAT
cp -f "$BASE_FOLDER_MDI/C_strelizia.mdi" "$BASE_FOLDER_DESTINATION/C_strelizia.mdi"
run_program $RUN_COMPILED_LIBRARY "$BASE_FOLDER_DESTINATION/C_strelizia.mdi" $BASE_ARG_DEBUG $BASE_ARG_FORMAT
# Module library with folder, destination and format
check_destination "$BASE_FOLDER/MODULE_FOLDER_DESTINATION_FORMAT"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/MODULE_FOLDER_DESTINATION_FORMAT" $BASE_ARG_FORMAT
# Module library with debug argument, folder, destination and format
check_destination "$BASE_FOLDER/MODULE_FOLDER_DESTINATION_FORMAT_DEBUG"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/MODULE_FOLDER_DESTINATION_FORMAT_DEBUG" $BASE_ARG_FORMAT $BASE_ARG_DEBUG
# Module library with folder and destination
check_destination "$BASE_FOLDER/MODULE_FOLDER_DESTINATION"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/MODULE_FOLDER_DESTINATION"
# Module library with debug argument, folder and destination
check_destination "$BASE_FOLDER/MODULE_FOLDER_DESTINATION_DEBUG"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER_MDI" "--destination=$BASE_FOLDER/MODULE_FOLDER_DESTINATION_DEBUG" $BASE_ARG_DEBUG
# Module library with folder
check_destination "$BASE_FOLDER/MODULE_FOLDER"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/MODULE_FOLDER"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER/MODULE_FOLDER"
# Module library with debug argument and folder
check_destination "$BASE_FOLDER/MODULE_FOLDER_DEBUG"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/MODULE_FOLDER_DEBUG"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER/MODULE_FOLDER_DEBUG" $BASE_ARG_DEBUG
# Module library with folder and format
check_destination "$BASE_FOLDER/MODULE_FOLDER_FORMAT"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/MODULE_FOLDER_FORMAT"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER/MODULE_FOLDER_FORMAT" $BASE_ARG_FORMAT
# Module library with debug argument, folder and format
check_destination "$BASE_FOLDER/MODULE_FOLDER_DEBUG_FORMAT"
cp -rf "$BASE_FOLDER_MDI" "$BASE_FOLDER/MODULE_FOLDER_DEBUG_FORMAT"
run_program $RUN_MODULE_LIBRARY "$BASE_FOLDER/MODULE_FOLDER_DEBUG_FORMAT" $BASE_ARG_DEBUG $BASE_ARG_FORMAT
echo "Testing completed."

# Cleaning up
echo "Cleaning up..."
rm -rf $BASE_FOLDER
if [ $? -ne 0 ]; then
    echo "Error: Failed to clean up test zone folder '$BASE_FOLDER'."
    exit $ERROR
fi
echo "Test zone folder cleaned up."

# Deactivate the virtual environment
if [ ! -z "$VIRTUAL_ENV" ]; then
    echo "Deactivating the virtual environment '$ENV_NAME'..."
    deactivate
    if [ $? -ne 0 ]; then
        echo "Error: Failed to deactivate the virtual environment '$ENV_NAME'."
        exit $ERROR
    fi
else
    echo "Virtual environment already deactivated."
fi
