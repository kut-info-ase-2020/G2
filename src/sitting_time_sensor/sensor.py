import RPi.GPIO as GPIO
class UninitializedError(Exception):
    def __init__(self, message):
        self.message = "Used before setup: " + message

class Sensor:
    INPUT      = GPIO.IN
    OUTPUT     = GPIO.OUT

    BCM_MODE   = GPIO.BCM
    BOARD_MODE = GPIO.BOARD

    port_map   = {}

    def setup(self, *, ports, port_settings, port_mode=BCM_MODE):
        GPIO.setwarnings(False)
        GPIO.setmode(port_mode)
        for (port, setting) in zip(ports, port_settings):
            if port in Sensor.port_map:
                print("Warning: overriding " + str(port) + " port setting")
            Sensor.port_map[port] = setting
            GPIO.setup(port, setting)

    def read(self, port):
        if not port in Sensor.port_map:
            raise UninitializedError("")
        if Sensor.port_map[port] != Sensor.INPUT:
            raise ValueError("port mode mismatch")
        return GPIO.input(port)

    def write(self, port, value):
        if port in Sensor.port_map:
            raise UninitializedError("")
        if Sensor.port_map[port] != Sensor.OUTPUT:
            raise ValueError("port mode mismatch")
        GPIO.output(port, value)

    def __init__(self, ports, port_modes, mapping_mode):
        self.setup(ports, port_modes, mapping_mode)
