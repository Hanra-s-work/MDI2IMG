color 0A
echo off
echo "Activating environment"
wenv\Scripts\activate & ^
echo "Building the project" & ^
python -m build & ^
echo "Installing the package" & ^
pip install dist\mdi2img-1.0.0.tar.gz & ^
echo "Running the project" & ^
python -m mdi2img %* & ^
echo "Deactivating environment" & ^
deactivate & ^
echo "Done"
pause
echo "(c) Written by Henry Letellier"
exit /b 0
REM End of script
