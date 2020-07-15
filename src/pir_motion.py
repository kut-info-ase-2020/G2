'''
	Motion detection using PIR on raspberry Pi
	http://www.electronicwings.com
'''
import RPi.GPIO as GPIO

PIR_input = 17				#read PIR Output
LED = 18
				#LED for signalling motion detected	
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)		#choose pin no. system
	GPIO.setup(PIR_input, GPIO.IN)	
	GPIO.setup(LED, GPIO.OUT)
	GPIO.output(LED, GPIO.LOW)

def main():
	while True:
		#when motion detected turn on LED
    		if(GPIO.input(PIR_input)):
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
