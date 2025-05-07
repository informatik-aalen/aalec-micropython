
# Micropython Firmware for the AALeC

This is the micropython implementation of the
[informatik-aalen/AALeC-V3](https://github.com/informatik-aalen/AALeC-V3)
Arduino library on GitHub.

The documentation of this library can be found at
[aalec-micropython](https://informatik-aalen.github.io/aalec-micropython) on GitHub Pages.

The stubs for this library can be found at
[aalec-micropython-stubs](https://pypi.org/project/aalec-micropython-stubs/)
on PyPi.

## Installation

It is recommended to use [uv](https://docs.astral.sh/uv/getting-started/) to
install the virtual python environment.

Please follow these five simple steps to install the micropython firmware for
your AALeC.

### 1\. Create a new project (`aalec-project`) with `uv`

```shell
uv init --lib aalec-project
```

### 2\. Install the stub files for the AALeC library

```shell
cd aalec-project
uv add aalec-micropython-stubs
```

### 3\. Download the micropython firmware

```shell
mkdir firmware
cd firmware
wget https://micropython.org/resources/firmware/ESP8266_GENERIC-20241129-v1.24.1.bin
cd ..
```

### 4\. Flash micropython to the ESP8266 on the AALeC

!!! danger

    Make sure you remove the jumper J2 before you attempt to use the esptool.
    Otherwise you will get an error that says, the ESP8266  can't be connected via serial port.

* Connect the ESP8266 on the AALeC with USB to your PC
* Erase the Flash with:

  ```shell
  uv run esptool.py --port /dev/ttyUSB0 erase_flash
  ```

* Flash micropython with:
  
  ```shell
  uv run esptool.py --port /dev/ttyUSB0 --baud 460800 \
            write_flash --flash_size=detect 0 \
            firmware/ESP8266_GENERIC-20241129-v1.24.1.bin
  ```

### 5\. Finally, install the `aalec-micropython` library on the AALeC

```shell
uv run mpremote mip install github:informatik-aalen/aalec-micropython
```

✨ Now is your AALeC ready to be used! ✨

Your project should now have the following file structure:

```dir
/
├── firmware
│   └── ESP8266_GENERIC-20241129-v1.24.1.bin
├── pyproject.toml
├── README.md
├── src
│   └── aalec_project
│       ├── __init__.py
│       └── py.typed
└── uv.lock
```

## Write your first program for the AALeC

Open your project in [Visual Studio Code](https://code.visualstudio.com/download) by typing the following command in your terminal:

```shell
code .
```

Create a new file in `src/aalec_project` with the name `first_program.py`

```python

import aalec

def hello_aalec():
    app = aalec.AALeC()

    app.print_line(3, "  Hello AALeC!")
    return app
```

Open a console in VSCode and upload the file to the AALeC:

```shell
uv run mpremote cp src/aalec_project/first_program.py :.
```

To start the program on the AALeC connect to the repl (*r*ead *e*valuate *p*rint *l*oop)

```shell
uv run mpremote

# Now you are in the repl

import first_program

first_program.hello_aalec()
```

Now your AALeC will show the text `Hello AALeC!` in the middle of its display.

You can exit the repl by pressing `<Strg> + <x>`.

🎉 Happy coding! 🎉

## 3rd Party Libraries

The AALeC library contains the following third party libraries:

The Library `sh1106.py` came from [https://github.com/robert-hh/SH1106](https://github.com/robert-hh/SH1106).

The Library `bmp280.py` came from [https://github.com/dafvid/micropython-bmp280](https://github.com/dafvid/micropython-bmp280).
