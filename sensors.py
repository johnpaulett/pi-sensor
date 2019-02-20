import adafruit_bmp3xx
import Adafruit_DHT
import adafruit_sgp30
import adafruit_tsl2591
import board
import busio


class Sensor(object):
    def __init__(self, i2c):
        self.i2c = i2c

    @property
    def name(self):
        return self.__class__.__name__

    def read(self):
        raise NotImplementedError()

    def safe_read(self):
        try:
            return self.read()
        except OSError as e:
            # TODO better logging than print()
            print('{}: {}'.format(self.name, e))
            return None


class I2CSensor(Sensor):
    sensor_cls = None  # Subclasses must implement

    def __init__(self, i2c):
        self.sensor = self.get_sensor(i2c)

    def get_sensor(self, i2c):
        return self.sensor_cls(i2c)


class BMP388(I2CSensor):
    """Pressure & Temperature Sensor"""
    sensor_cls = adafruit_bmp3xx.BMP3XX_I2C
    units = {
        'pressure': 'Pa',
        'temperature': 'C',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO make oversampling configurable
        self.sensor.pressure_oversampling = 8  # High Resolution (0.33Pa)
        self.sensor.temperature_oversampling = 2  # (0.0025C)

    def read(self):
        return {
            'pressure': self.sensor.pressure,
            'temperature': self.sensor.temperature
        }


class DHT22(Sensor):
    units = {
        'humidity': 'percent',
        'temperature': 'C',
    }

    def __init__(self, pin):
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin if isinstance(pin, int) else pin.id

    def read(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin)
        # Adafruit_DHT.read_retry(dht, board.D4)
        return {
            'humidity': humidity,
            'temperature': temperature,
        }


# import adafruit_mcp9808

# class MCP9808(I2CSensor):
#     """High precision Temperature Sensor"""
#     sensor_cls = adafruit_mcp9808.MCP9808
#     units = {
#         'temperature': 'C',
#     }

#     def read(self):
#         return {
#             'temperature': self.sensor.temperature
#         }


class SGP30(I2CSensor):
    """Air Quality Sensor"""
    sensor_cls = adafruit_sgp30.Adafruit_SGP30
    units = {
        'eco2': 'ppm',
        'tvoc': 'ppb',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sensor.iaq_init()

        # TODO set baseline from prior readings or it will take 12 hours to get ready
        # self.sensor.set_iaq_baseline(0x8973, 0x8aae)

    def read(self):
        # TODO take in humidity
        # self.sensor.set_iaq_humidity(gramsPM3)

        # TODO after 12 hrs store baseline every ~10 seconds (persist, can be
        #   by [hex(i) for i in sgp30.serial])
        # co2eq_base, tvoc_base = sgp30.baseline_co2eq, sgp30.baseline_tvoc

        # FIXME per datasheet readings should occur at 1Hz (we're doing 0.2Hz)

        eCO2, TVOC = self.sensor.iaq_measure()

        return {
            'eco2': eCO2,
            'tvoc': TVOC,
        }


class TSL2591(I2CSensor):
    """Luminosity Sensor"""
    sensor_cls = adafruit_tsl2591.TSL2591
    units = {
        'lux': 'lux',
        'visible': '',  # TODO What unit are these in?
        'infrared': '',
        'full_spectrum': '',
    }

    # TODO allow configuration of the gain / integration_time

    def read(self):
        return {
            'lux': self.sensor.lux,
            'visible': self.sensor.visible,
            'infrared': self.sensor.infrared,
            'full_spectrum': self.sensor.full_spectrum,
        }


def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    # TODO use i2c.scan() to detect which sensors are plugged in

    sensors = [
        BMP388(i2c),
        DHT22(25),
        # MCP9808(i2c),
        SGP30(i2c),
        TSL2591(i2c),
    ]

    from prometheus_client import start_http_server, Gauge  # Summary
    import time
    start_http_server(8000)

    metrics = {}
    for sensor in sensors:
        for metric, unit in sensor.units.items():
            name = sensor.name + '_' + metric
            metrics[name] = Gauge(name, unit)  # Summary

    while True:
        result = {sensor.name: sensor.safe_read() for sensor in sensors}
        print(result)

        for sensor_name, data in result.items():
            if data is None:  # When safe_read() has an error
                continue

            for metric, value in data.items():
                if value is not None:
                    # metrics[sensor_name + '_' + metric].observe(value)
                    metrics[sensor_name + '_' + metric].set(value)
        time.sleep(5)


if __name__ == '__main__':
    main()
