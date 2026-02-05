# This is a dockerfile provided to help linux and mac users run the library by providing the required environement for the windows binary the library relies on can run.

# Using the busybox image to have binaries that are compatible with the linux image in case they get stripped by the build process.
FROM busybox:1.37.0-uclibc AS binary_base

# Using the official python image as the base image in the container.
FROM python:3.14.3-slim-bookworm

# Setting the DEBIAN_FRONTEND noninteractive environment variable to avoid any interactive prompts during package installation or runtime.
ENV DEBIAN_FRONTEND=noninteractive

# Set up Wine environment
# |- Wine architecture
ENV WINEARCH=win32
# |- Wine user account name
ARG WINE_USER=wineuser
# \- Wine prefix (the directory where Wine stores its configuration and installed applications)
ENV WINEPREFIX="/home/${WINE_USER}/.wine"

# Get the root password for the image.
ARG ROOT_PASSWD=root

# Set the root password for the image.
RUN echo "root:${ROOT_PASSWD}" | chpasswd

# Set environment variables to prevent X11 errors
ENV DISPLAY=:0
ENV XDG_RUNTIME_DIR=/tmp

# Update pip
RUN pip install --upgrade pip

# Setting the busybox directory if the image is being built as a standalone image.
ARG busybox_bin_path=/busybox

# Add the colour for the ls command
RUN echo "alias ls='ls --color=auto'" >> /etc/bash.bashrc

# Make sure the keyrings directory exists
RUN mkdir -pm755 /etc/apt/keyrings

# Updating the system's repository list
RUN apt update

# Install wget, sudo and gnupg2 as well as the debian base dependencies for a more "stable" system.
RUN apt install -y wget gnupg2  software-properties-common sudo

# Create a wine user
RUN useradd -m ${WINE_USER} \
    && usermod -aG sudo ${WINE_USER} \
    && echo "${WINE_USER}:${WINE_USER}" | chpasswd \
    && echo "${WINE_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Add the 32 bit architecture to the system
RUN dpkg --add-architecture i386

# Adding the winehq key to the system's keyring
RUN wget -O - https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor -o /etc/apt/keyrings/winehq-archive.key -

# Adding the wine repository to the system's sources list
RUN wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources

# Installing winetricks manually as the package is not available in the debian repository.
RUN wget -O /usr/local/bin/winetricks https://raw.githubusercontent.com/Winetricks/winetricks/refs/heads/master/src/winetricks \
    && chmod +x /usr/local/bin/winetricks

# Updating the list
RUN apt update

# Install the required x11 libraries for Wine to run
RUN apt install -y x11-utils xauth xserver-xorg-core xinit xvfb x11vnc fluxbox

# Add Install the 32bit version if wine is in that mode, otherwise install the 64bit version.
RUN apt update && if [ "${WINEARCH}" = "win32" ]; then apt install -y libvulkan1:i386 mesa-vulkan-drivers:i386 vulkan-tools:i386; \
    else apt install -y libvulkan1 mesa-vulkan-drivers vulkan-tools; \
    fi

# Installing the required wine packages for the python library to run.
RUN apt install -y --install-recommends winehq-stable cabextract winbind

# A fix for the temporary folder (just in case)
RUN rm -rf /tmp && mkdir -p /tmp && chmod 1777 /tmp

# Create the X11 socket directory
RUN mkdir -p /tmp/.X11-unix \
    && chmod 1777 /tmp/.X11-unix

# Switch to the wine user
USER ${WINE_USER}

# Go to the home directory of the wine user
WORKDIR /home/${WINE_USER}

# Switch to the root user
USER root

# Run the windbind command to create the required directories for the wine prefix.
RUN winbindd

# Switch back to the wine user
USER ${WINE_USER}

# Create a bash entrypoint script to start the X11 server and the VNC server.
RUN echo '#!/bin/bash\n' \
    '# Running winbindd to create the required directories for the wine prefix\n' \
    'echo "Starting winbindd..."\n' \
    'sudo winbindd &\n' \
    '# Start virtual framebuffer\n' \
    'echo "Starting Xvfb..."\n' \
    'sudo Xvfb :0 -screen 0 1024x768x16 &\n' \
    'if [ $? -ne 0 ]; then\n' \
    '    STATUS=$?' \
    '    echo "Failed to start Xvfb, status $STATUS"\n' \
    '    exit $STATUS\n' \
    'else\n' \
    '    echo "Xvfb status: $?";\n' \
    '    echo "Xvfb started successfully";\n' \
    'fi\n' \
    '# Give Xvfb a moment to start\n' \
    'echo "Waiting for Xvfb to start..."\n' \
    'sleep 2\n' \
    '# Start a window manager (or Wine GUIs may crash)\n' \
    'echo "Starting Fluxbox..."\n' \
    'fluxbox &\n' \
    'if [ $? -ne 0 ]; then\n' \
    '    STATUS=$?' \
    '    echo "Failed to start fluxbox, status $STATUS"\n' \
    '    exit $STATUS\n' \
    'else\n' \
    '    echo "Fluxbox status: $?";\n' \
    '    echo "Fluxbox started successfully";\n' \
    'fi\n' \
    '# Start the VNC server on display :0, no password for now\n' \
    'echo "Starting x11vnc..."\n' \
    'x11vnc -display :0 -nopw -listen 0.0.0.0 -forever &\n' \
    'if [ $? -ne 0 ]; then\n' \
    '    STATUS=\$?' \
    '    echo "Failed to start x11vnc, status $STATUS"\n' \
    '    exit $STATUS\n' \
    'else\n' \
    '    echo "x11vnc status: $?";\n' \
    '    echo "x11vnc started successfully";\n' \
    'fi\n' \
    '# Set DISPLAY so Wine apps know where to draw\n' \
    'echo "Setting DISPLAY variable..."\n' \
    'export DISPLAY=:0\n' \
    '# starting a bash instance\n' \
    'echo "Starting bash..."\n' \
    'python -c "import tkinter as tk;tk.Tk();tk.mainloop()"' \
    'exec "$@"' > /home/${WINE_USER}/entrypoint.sh \
    && chmod +x /home/${WINE_USER}/entrypoint.sh


# Start an x11 screen server
# RUN export DISPLAY=:0 && sudo Xvfb :0 -screen 0 1024x768x16 &

# Ensure Wine is set up before installing Mono
# RUN sleep 2 && DISPLAY=:0 wineboot --init &

# Check that the screen is up an running
# RUN sleep 2 && DISPLAY=:0 xset q

# Booting wine server
# RUN sleep 5 && wineserver -w &

# Specifying the version of Wine Mono to be installed. This is the version that is compatible with the Wine version in the image.
# ARG MONO_VERSION=10.0.0

# Install Wine Mono (for .NET apps)
# RUN wget https://dl.winehq.org/wine/wine-mono/${MONO_VERSION}/wine-mono-${MONO_VERSION}-x86.msi && \
# wine msiexec /i wine-mono-${MONO_VERSION}-x86.msi && \
# rm wine-mono-${MONO_VERSION}-x86.msi


# Switching back to root for some final touches
USER root

# Copying the busybox binaries from the busybox image to the current image.
RUN mkdir -p ${busybox_bin_path}
COPY --from=binary_base /bin ${busybox_bin_path}

# removing the busybox binaries if the image is being used as a base.
ONBUILD RUN rm -rf ${busybox_bin_path}

# Debug binaries
RUN apt install -y curl nano net-tools htop

# Removing apt cache
ONBUILD RUN apt clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*

# Switching back to the wine user
USER wineuser

# For debugging (in case of a graphical window)
EXPOSE 5900

# The entrypoint of the script
# CMD [ "/home/wineuser/entrypoint.sh" ]
