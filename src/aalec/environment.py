"""Environment utilities."""

import machine  # type: ignore
import aalec.third_party.bmp280 as bmp280


class Environment:
    """Environment class.

    Args:
        i2c: A `machine.I2C` instance.
        addr: The i2c address of the sensor.
    """

    def __init__(self, i2c: machine.I2C, addr: int):
        self._i2c: machine.I2C = i2c
        self._addr: int = addr
        self._bmp280: bmp280.BMP280 = bmp280.BMP280(self._i2c, self._addr)

    def get_environment_sensor(self) -> str:
        """Get type of environment sensor

        Returns:
            str: "BMP280"
        """
        return "BMP280"

    def get_temp(self) -> float:
        """Get current Temperature.

        Returns:
            float: Current temperature in °C.
        """
        self._bmp280.normal_measure()
        return self._bmp280.temperature

    def get_humidity(self) -> float:
        """Get current humidity.

        Returns:
            float: 0.0 (BMP280 doesn't have a humidity sensor).
        """
        return 0.0

    def get_pressure(self) -> float:
        """Get current pressure in hPa.

        Returns:
            float: current pressure in hPa.
        """
        self._bmp280.normal_measure()
        return self._bmp280.pressure / 100.0

    def get_gas_resistance(self) -> float:
        """Get gas resistance.

        Returns:
            float: 0.0 (BMP280 doesn't have a gas resistance sensor).
        """
        return 0.0


def test_environment() -> None:
    """Test for the environment class."""
    from time import sleep
    from aalec import constants

    i2c = machine.I2C(
        scl=machine.Pin(constants.PIN_SCL), sda=machine.Pin(constants.PIN_SDA)
    )
    environment = Environment(i2c, constants.BMP280_ADDR)
    while True:
        print(f"Sensor:            {environment.get_environment_sensor()}")
        print(f"Temperature:       {environment.get_temp()} °C")
        print(f"Relative Humidity: {environment.get_humidity()} %")
        print(f"Pressure:          {environment.get_pressure()} hPa")
        print(f"Gas resistance:    {environment.get_gas_resistance()}")
        print(10 * "-")
        sleep(2)
