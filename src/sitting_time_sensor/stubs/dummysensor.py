from sys import stderr
from collections import namedtuple

class PIRSensor:
    Status = namedtuple('Status', ['changed', 'unchanged'])
    status = Status(changed=1, unchanged=0) # 暫定
    switch_port = -1
    read_value = 0
    wrote_value = 0
    read_num = 0
    def read(self):
        PIRSensor.read_num += 1
        if PIRSensor.read_num > 10:
            PIRSensor.read_num = 0
            if PIRSensor.read_value == 0:
                PIRSensor.read_value = 1
            else:
                PIRSensor.read_value = 0
        print("dummy sensor: read " + str(PIRSensor.read_value) + " from " + str(PIRSensor.switch_port) + " port", file=stderr)
        return PIRSensor.read_value
    def write(self, port, value):
        print("dummy sensor: write " + str(value) + " to " + str(port) + "port", file=stderr)
        PIRSensor.wrote_value = value
    def setup(self, port):
        PIRSensor.switch_port = port

    def __init__(self, port):
        self.setup(port)
    def destroy(self):
        pass
