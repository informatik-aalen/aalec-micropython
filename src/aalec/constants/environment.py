"""Environment constants."""

from micropython import const  # type: ignore


BMP280_ADDR: int = const(0x76)
"""I2C addresses for the sensors."""
