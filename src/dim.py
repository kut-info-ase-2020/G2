import RPi.GPIO as GPIO
import time

#DHT11 connect to BCM_GPIO14
DHTPIN = 14
BAD_LED_PIN = 27
NORMAL_LED_PIN = 18
GOOD_LED_PIN = 17
LED_PINS = [BAD_LED_PIN, NORMAL_LED_PIN, GOOD_LED_PIN]

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set LEDPIN's mode to output,and initial level to LOW(0V)
    for PIN in LED_PINS:
        GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

def read_dht11_dat():
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(DHTPIN)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        print "Data not good, skip"
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    # print "bits: %s, length: %d" % (bits, len(bits))
    for i in range(0, len(bits)):
        byte = byte << 1
        if (bits[i]):
            byte = byte | 1
        else:
            byte = byte | 0
        if ((i + 1) % 8 == 0):
            the_bytes.append(byte)
            byte = 0
    print the_bytes
    checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        print "Data not good, skip"
        return False

    return the_bytes[0], the_bytes[2]

def calc_discomfort_index(humidity, temperature):
    return 0.81 * temperature + 0.01 * humidity * (0.99 * temperature - 14.3) + 46.3

def main():
    print "Discomfort index meter\n"
    while True:
        result = read_dht11_dat()
        if result:
            humidity, temperature = result
            disc_idx = calc_discomfort_index(humidity, temperature)
            print "humidity: %s %%,  Temperature: %s C" % (humidity, temperature)
            print ("Idx: " + str(disc_idx))
            for PIN in LED_PINS:
                GPIO.output(PIN, GPIO.LOW)
            if (disc_idx <= 75):
                print ("GOOD")
                GPIO.output(GOOD_LED_PIN, GPIO.HIGH)
            elif (75 < disc_idx && disc_idx < 85):
                print ("NORMAL")
                GPIO.output(NORMAL_LED_PIN, GPIO.HIGH)
            else:
                print ("BAD")
                GPIO.output(BAD_LED_PIN, GPIO.HIGH)
        time.sleep(1)

def destroy():
    for PIN in LED_PINS:
        GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy() 

