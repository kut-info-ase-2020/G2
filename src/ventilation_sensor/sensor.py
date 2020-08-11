import RPi.GPIO as GPIO
class Sensor:
    INPUT      = GPIO.IN
    OUTPUT     = GPIO.OUT

    BCM_MODE   = GPIO.BCM
    BOARD_MODE = GPIO.BOARD

    port_map   = {}

    class UninitializedError(Exception):
        def __init__(self, message):
            self.message = "Used before setup: " + message

    def setup(self, *, ports, port_settings, port_mode=BCM_MODE):
        GPIO.setwarnings(False)
        GPIO.setmode(port_mode)
        for (port, setting) in zip(ports, port_settings):
            if port in port_map:
                print("Warning: overriding " + str(port) + " port setting")
            Sensor.port_map[port] = setting
            GPIO.setup(port, setting)

    def read(port):
        if port in Sensor.port_map:
            raise UninitializedError("")
        if port_map[port] != Sensor.INPUT:
            raise ValueError("port mode mismatch")
        return GPIO.input(port)

    def write(port, value):
        if port in Sensor.port_map:
            raise UninitializedError("")
        if port_map[port] != Sensor.OUTPUT:
            raise ValueError("port mode mismatch")
        GPIO.output(port, value)

    def __init__(self, ports, port_modes, mapping_mode):
        self.setup(ports, port_modes, mapping_mode)
