# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import csv
from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta
import statistics
import time
import os

from SlackAPI import SlackAPI_class
#token=os.environ['SLACK_API_TOKEN']
#channels = '#zikkenzyou_go'

class calWBGT():
    def __init__(self): 
        self.api = SlackAPI_class.SlackAPI(
            token=os.environ['SLACK_API_TOKEN'], 
            channels = '#zikkenzyou_go'
            )

        self.notified_flag = False

    def calWBGT(self, csv_path):

        #センシングを行う回数
        countSensing = 10
        #故障時に備えたループの最大回数
        countMaxSensing = 1000
        #タイムゾーンの生成とセンシングした時刻を計測
        JST = timezone(timedelta(hours=+9), 'JST')
        dt_now = datetime.now(JST)
        dt_now = datetime.now()
        datatime = dt_now.strftime('%H:%M:%S')
        #WBGTと気温と湿度のデータ格納配列
        dataWBGT = []
        datatemperature = []
        datahumidity = []

        #ここから指定の回数分だけセンサーのデータを取り出します
        while True:
            #ここでセンシングを行う
            countMaxSensing-=1
            result = self.read_dht11_dat()
            if result:
                #うまくセンサーの値が一回取れた場合
                countSensing-=1
                humidity, temperature = result
                print(humidity)
                disc_idx = self.calc_discomfort_index(humidity, temperature)
                dataWBGT.append(disc_idx)
                datatemperature.append(temperature)
                datahumidity.append(humidity)
            if countSensing == 0:
                #指定の回数分のデータが取れた場合
                #データの中央値を取り出す
                a = statistics.median(dataWBGT)
                b = statistics.median(datatemperature)
                c = statistics.median(datahumidity)
                with open(csv_path, 'a') as f:
                    writer = csv.writer(f)

                    writer.writerow([datatime, c, b, a])
                if a > 25 and self.notified_flag == False:
                    self.api.Notification_HeatStroke(b,c)
                    self.notified_flag = True
                    #WBGTが危険の場合、1を返す
                    return 1
                else:
                    self.notified_flag = False
                    """
                    api.Notification_HeatStroke(b,c)
                    """
                    return 0
            if countMaxSensing == 0:
                with open(csv_path, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([datatime, -1, -1, -1])
                return -1

    def read_dht11_dat(self):
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
        GPIO.setwarnings(False)
        #set the gpio modes to BCM numbering
        GPIO.setmode(GPIO.BCM)
        #set LEDPIN's mode to output,and initial level to LOW(0V)
        for PIN in LED_PINS:
            GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

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
            #print "Data not good, skip"
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
        #print the_bytes
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            #print "Data not good, skip"
            return False

        return the_bytes[0], the_bytes[2]

    def calc_discomfort_index(self, humidity, temperature):
        return 0.725 * temperature + 0.0368 * humidity + 0.00364 * temperature *humidity - 3.246
