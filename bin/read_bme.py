import smbus2
import bme280
from datetime import datetime as dt

port = 1
address = 0x76
bus = smbus2.SMBus(port)

def read_bme280():
    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    # # the compensated_reading class has the following attributes
    # print(data.id)
    # print(data.timestamp)
    # print(data.temperature)
    # print(data.pressure)
    # print(data.humidity)

    # # there is a handy string representation too
    # print(data)

    return {
        'ts': dt.timestamp(data.timestamp),
        'temp': data.temperature,
        'pressure': data.pressure,
        'humidity': data.humidity
    }
