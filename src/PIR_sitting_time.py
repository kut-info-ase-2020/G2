#import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import csv
import os

from SlackAPI.SlackAPI_class import SlackAPI
from sched import scheduler

class PIR_sensor():
    def __init__(self):
        # set BCM_GPIO 17(wPi#0) as PIR pin
        self.PIRPin = 16
        # set BCM_GPIO 18(wPi#1) as buzzer pin
        self.BuzzerPin = 26

        self.pir_flag = 0
        self.nalarm_count = 0
        self.sitting_count = 0
        self.alarm = datetime.now()
        self.sitting_start = datetime.now()

        self.api = SlackAPI(
            token=os.environ['SLACK_API_TOKEN'], 
            channels = '#zikkenzyou_go'
            )

        self.current = datetime.now().replace(microsecond=0) # for test
        self.next_time = self.current
        self.today = date.today()
        self.export_csv_name = "sitting-" + str(self.today.year) + "-" + str(self.today.month) + "-" + str(self.today.day) + ".csv"
        if not os.path.exists(self.export_csv_name):
            with open(self.export_csv_name, 'a') as f:
                writer = csv.writer(f)

    #print message at the begining ---custom function
    def print_message(self):
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
    def setup(self):
        GPIO.setwarnings(False)
        #set the gpio modes to BCM numbering
        GPIO.setmode(GPIO.BCM)
        #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
        GPIO.setup(self.BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.PIRPin,GPIO.IN)

    def detect_Human(self, pin):
        #input = GPIO.input(PIRPin)
        input = 1
        if(input != 0):
            if(pir_flag == 0):
                self.sitting_start = datetime.datetime.now()
                self.nalarm_count = 0
                now1 = datetime.datetime.now()
                with open(self.export_csv_name, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([str(now1.hour)+str(now1.minute), 1])
                pir_flag = 1
                print("pir_flag:"+str(pir_flag)+"\n")
                GPIO.output(self.BuzzerPin,GPIO.LOW)
                #time.sleep(0.5)
                #print ('********************')
                #print ('*     alarm!     *')
                #print ('********************')
            else:
                now_time = datetime.datetime.now()
                elapsed_time = now_time - self.alarm
                print("elapsed_time:"+str(elapsed_time))
                if(elapsed_time.seconds < 60):
                    self.nalarm_count += 1
                    print("nalarm_count:"+str(self.nalarm_count))
                    print("pir_flag:"+str(pir_flag))
                    GPIO.output(self.BuzzerPin,GPIO.HIGH)
                    #print ('====================')
                    #print ('=     Not alarm...  =')
                    #print ('====================')
                    print ('\n')
                else:
                    if(self.nalarm_count > 45):
                        sitting_time = datetime.datetime.now() - self.sitting_start
                        print("sitting time:"+str(sitting_time)+"[sec]")
                        pir_flag = 0
                        print("pir_flag:"+str(pir_flag))
                        now2 = datetime.datetime.now()
                        with open('Sitting.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([now2.ToString("HHmm"), 0])
                    else:
                        self.sitting_count += 1
                        if self.sitting_count > 5:
                            sitting_time_amount = datetime.datetime.now() - self.sitting_start
                            self.api.Notification_Sitting(int(sitting_time_amount.total_seconds() / 60))
                    self.alarm = datetime.datetime.now()
                    nalarm_count = 0

    def timer_loop():
        if not os.path.exists(export_csv_name):
            with open(export_csv_name, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['date','Hum','Temp','WBGT'])

        print_message()
        # Create CSV file
        with open(export_csv_name, 'a') as f:
            writer = csv.writer(f)
            #writer.writerow(["time", "0 or 1"])

        while True:
            timer_sched.enterabs(next_time.timestamp(), 1, detect_Human, kwargs={'pin': PIRPin})
            timer_sched.run()
            # if today < date.today():
            if current + timedelta(minutes=3) < datetime.now():
                api.Visualization_Sitting(path=export_csv_name)
                today = date.today()
                export_csv_name = "sitting-" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".csv"
                with open(export_csv_name, 'w') as f:
                    writer = csv.writer(f)
                current = datetime.now().replace(microsecond=0)
            # next_time = current + timedelta(minutes=30)
            next_time = current + timedelta(seconds=1)

    #define a destroy function for clean up everything after the script finished
    def destroy(self):
        #turn off buzzer
        GPIO.output(self.BuzzerPin,GPIO.HIGH)
        #release resource
        GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    sensor = PIR_sensor()
    sensor.setup()
    try:
        sensor.timer_loop()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        sensor.destroy()
        pass
