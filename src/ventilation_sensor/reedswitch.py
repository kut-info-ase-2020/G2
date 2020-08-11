from sensor import Sensor
import RPi.GPIO as GPIO

class ReedSwitch(Sensor):
    MFStatus = namedtuple('MFStatus', ['strong', 'weak'])
    mfstatus = MFStatus(strong=0, weak=1) # 暫定
    switch_port = -1

    def setup(self, *, port):
        super().setup(ports=[port], port_settings=[super().INPUT])
        ReedSwitch.switch_port = port

    def read():
        read_val = super().read(switch_port)
        if (read_val == mfstatus.strong):
            return 1
        return 0

    def main(self):
        while True:
            time.sleep(1)
            #when motion detected turn on LED
            input = self.read()
            print("reed switch input:", input)

    def destroy():
        GPIO.cleanup()

    def __init__(self, port):
        setup(port)

if __name__ == '__main__':
    reed_switch = ReedSwitch.setup(port=26)
    try:
        reed_switch.main()
    except KeyboardInterrupt:
        reed_switch.destroy() 
