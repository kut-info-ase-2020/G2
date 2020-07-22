import RPi.GPIO as GPIO
import time
leed_input = 26
LED = 18

def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    #GPIO.setmode(GPIO.BOARD)		#choose pin no. system
    GPIO.setup(leed_input, GPIO.IN)	
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.LOW)

def main():
    while True:
        time.sleep(1)
        #when motion detected turn on LED
        input = GPIO.input(leed_input)
        print(input)
        if(!input):
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy() 
