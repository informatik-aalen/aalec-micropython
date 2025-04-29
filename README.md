# Micropython Firmware for the AALeC

This is the micropython implementation of the
[informatik-aalen/AALeC-V3](https://github.com/informatik-aalen/AALeC-V3)
Arduino library on GitHub.

The documentation of this library can be found at
[https://informatik-aalen.github.io/AALeC-micropython](https://informatik-aalen.github.io/AALeC-micropython)

## Installation

It is recommended to use [uv](https://docs.astral.sh/uv/getting-started/) to
install the virtual python environment.

First clone this repository:

```bash
git clone https://github.com/informatik-aalen/AALeC-micropython.git
```

Create the virtual environment:

```bash
cd AALeC-micropython
uv sync
```

Finally activate the virtual environment:

```bash
. .venv/bin/activate
```

The following steps require an activated virtual environment!

### First Setup

The following two steps are only required for the initial setup of the AALeC.
Afterwards you only need to upload your python files.

#### Flash Micropython on the Microcontroller

Connect the AALeC with your PC with a USB-cable and flash the Micropython
firmware to the ESP8266 of the AALeC.
The current tested version of Micropython can be found in the `firmware`
directory of this repository:

```shell
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 \
        write_flash --flash_size=detect 0 \
        firmware/ESP8266_GENERIC-20241129-v1.24.1.bin
```

#### Install this library on the Microcontroller

The last step is to upload the AALeC Library to the ESP8266 of the AALeC:

```bash
mpremote mip install ./package.json
```

## Your first project with the AALeC Library

Open a new terminal and create a new project (with the name `new_project`).

!!! Warning

    Please make sure that you **don't** put your new project as a subdirectory
    of this repository!
    
```shell
# Initialize the new project
uv init --lib aalec_project

# Install the stubs for this library
cd aalec_project
uv add aalec-micropython-stubs

# Open the project in VSCode:
code .
```

Put your python files in the `src/new_project` directory.

!!! example

    You have written your code in `src/new_project/my_file.py`.
    
    Then you can open a terminal in VSCode, activate the virtual environment,
    and upload this file to the AALeC with:
    
    ```bash
    mpremote cp src/new_project/my_file.py :my_file.py
    ```

## 3rd Party Libraries

The AALeC library contains the following third party libraries:

The Library `sh1106.py` came from [https://github.com/robert-hh/SH1106](https://github.com/robert-hh/SH1106).

The Library `bmp280.py` came from [https://github.com/dafvid/micropython-bmp280](https://github.com/dafvid/micropython-bmp280).
