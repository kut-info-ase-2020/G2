import RPi.GPIO as GPIO
import time
import datetime
import csv

from SlackAPI import SlackAPI_class

# set BCM_GPIO 17(wPi#0) as PIR pin
PIRPin = 16
# set BCM_GPIO 18(wPi#1) as buzzer pin
BuzzerPin = 26

#print message at the begining ---custom function
def print_message():
    print ('==================================')
    print ('|              Alarm             |')
    print ('|     -----------------------    |')
    print ('|     PIR connect to GPIO0       |')
    print ('|                                |')
    print ('|     Buzzer connect to GPIO1    |')
    print ('|     ------------------------   |')
    print ('|                                |')
    print ('|                          OSOYOO|')
    print ('==================================\n')
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(PIRPin,GPIO.IN)

#main function
def main():
#print info
    print_message()
    # Create CSV file
    with open('Sitting.csv', 'w') as f:
        writer = csv.writer(f)
        #writer.writerow(["time", "0 or 1"])
    pir_flag = 0
    nalarm_count = 0
    sitting_count = 0
    global alarm
    alarm = datetime.datetime.now()
    while True:
        #read Sw520dPin's level
	input = GPIO.input(PIRPin)
	print(input)
        if(input != 0):
            if(pir_flag == 0):
                alarm = datetime.datetime.now()
                nalarm_count = 0
                now1 = datetime.datetime.now()
                with open('Sitting.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([str(now1.hour)+str(now1.minute), 1])
            #nalarm_count = 0
            pir_flag = 1
            print("pir_flag:"+str(pir_flag))
            GPIO.output(BuzzerPin,GPIO.LOW)
            #time.sleep(0.5)
            #print ('********************')
            #print ('*     alarm!     *')
            #print ('********************')
            print ('\n')
            time.sleep(1)
        else:
            now_time = datetime.datetime.now()
            elapsed_time = now_time - alarm
            print("elapsed_time:"+str(elapsed_time))
            if(elapsed_time.seconds < 60):
                nalarm_count += 1
                print("nalarm_count:"+str(nalarm_count))
                print("pir_flag:"+str(pir_flag))
                GPIO.output(BuzzerPin,GPIO.HIGH)
                #print ('====================')
                #print ('=     Not alarm...  =')
                #print ('====================')
                print ('\n')
                time.sleep(1)
            else:
                if(nalarm_count > 45):
                    sitting_time = datetime.datetime.now() - alarm
                    print("sitting time:"+str(sitting_time)+"[sec]")
                    pir_flag = 0
                    print("pir_flag:"+str(pir_flag))
                    now2 = datetime.datetime.now()
                    with open('Sitting.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([str(now2.hour)+str(now2.minute), 0])
                else:
                    sitting_count += 1
                    if sitting_count > 5:
                        api = SlackAPI_class.SlackAPI(
                            token=os.environ['SLACK_API_TOKEN'],
                            channels = '#zikkenzyou_go'
                            )
                        api.Notification_Sitting(datetime.datetime.now() - alarm)
                        return 1
                alarm = datetime.datetime.now()
                nalarm_count = 0
#define a destroy function for clean up everything after the script finished
def destroy():
    #turn off buzzer
    GPIO.output(BuzzerPin,GPIO.HIGH)
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass
