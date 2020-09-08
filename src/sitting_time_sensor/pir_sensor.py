import time
from collections import namedtuple
from sitting_time_sensor.sensor import Sensor
import RPi.GPIO as GPIO

class PIRSensor(Sensor):
    Status = namedtuple('Status', ['changed', 'unchanged'])
    status = Status(changed=1, unchanged=0) # 暫定
    sensor_port = -1

    def setup(self, port):
        super().setup(ports=[port], port_settings=[super().INPUT])
        PIRSensor.sensor_port = port

    def read(self):
        read_val = super().read(PIRSensor.sensor_port)
        if (read_val == PIRSensor.status.changed):
            return 1
        return 0

    def main(self):
        while True:
            time.sleep(1)
            #when motion detected turn on LED
            input = self.read()
            print("PIR sensor input:", input)
            if input == 1:
                print("detected")
            else:
                print("not detected")

    def destroy(self):
        GPIO.cleanup()

    def __init__(self, port):
        self.setup(port)

if __name__ == '__main__':
    pir_sensor = PIRSensor(port=26)
    try:
        pir_sensor.main()
    except KeyboardInterrupt:
        pir_sensor.destroy() 
