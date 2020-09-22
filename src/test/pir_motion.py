'''
	Motion detection using PIR on raspberry Pi
	http://www.electronicwings.com
'''
import RPi.GPIO as GPIO
import time
PIR_input = 17				#read PIR Output
LED = 18
				#LED for signalling motion detected	
def setup():
	GPIO.setwarnings(False)
	#set the gpio modes to BCM numbering
    	GPIO.setmode(GPIO.BCM)
	#GPIO.setwarnings(False)
	#GPIO.setmode(GPIO.BOARD)		#choose pin no. system
	GPIO.setup(PIR_input, GPIO.IN)	
	GPIO.setup(LED, GPIO.OUT)
	GPIO.output(LED, GPIO.LOW)

def main():
	while True:
		time.sleep(1)
		#when motion detected turn on LED
		input = GPIO.input(PIR_input)
		print(input)
    		if(input):
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
