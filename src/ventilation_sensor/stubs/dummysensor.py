from sys import stderr
from collections import namedtuple

class ReedSwitch:
    MFStatus = namedtuple('MFStatus', ['strong', 'weak'])
    mfstatus = MFStatus(strong=0, weak=1) # 暫定
    switch_port = -1
    read_value = 0
    wrote_value = 0
    read_num = 0
    def read(self):
        ReedSwitch.read_num += 1
        if ReedSwitch.read_num > 10:
            ReedSwitch.read_num = 0
            if ReedSwitch.read_value == 0:
                ReedSwitch.read_value = 1
            else:
                ReedSwitch.read_value = 0
        print("dummy sensor: read " + str(ReedSwitch.read_value) + " from " + str(ReedSwitch.switch_port) + " port", file=stderr)
        return ReedSwitch.read_value
    def write(self, port, value):
        print("dummy sensor: write " + str(value) + " to " + str(port) + "port", file=stderr)
        ReedSwitch.wrote_value = value
    def setup(self, port):
        ReedSwitch.switch_port = port

    def __init__(self, port):
        self.setup(port)
    def destroy(self):
        pass
