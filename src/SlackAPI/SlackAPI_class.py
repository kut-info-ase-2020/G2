import os
import slack
import numpy as np
import pandas as pd
import io
from slack import WebClient
from slack import RTMClient
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
from slack.errors import SlackApiError

class SlackAPI:
    def __init__(self, token,channels):
        self.client = slack.WebClient(token)
        self.channels = channels
        self.token = token
        print("setting finish")

    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(
                channel=self.channels,
                text=message
            )
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]

    def Notification_send(self,text):
        try:
            print("notification send!")
            #warningを通知
            response = self.client.chat_postMessage(
                channel=self.channels,
                text=text
            )
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]
    def Notification_Sitting(self,time):
        try:
            print("PIR notification message create...")
            message = "椅子に座りすぎです！椅子から立ち、軽い運動を試みてください！\n連続で座っていた時間 = " + str(time) + "分"
            self.Notification_send(message)
        except IndexError:
            print("エラー！引数に不正があります")
    def Notification_Ventilation(self,time):
        try:
            print("Ventilate notification message create...")
            message = "しばらくの間換気が行われていません！窓を開けて換気を試みてください！\n窓が閉まっていた時間 = " + str(time) + "分"
            self.Notification_send(message)
        except IndexError:
            print("エラー！引数に不正があります")

    def Notification_HeatStroke(self,Temp,Hum):
        try:
            print("Heatstroke notification message create...")
            message = "熱中症の危険があります！窓を開ける、エアコンを起動するなどの対策を行ってください！\n室温 = "+ str(Temp) + "度\n湿度 = " + str(Hum) + "度"
            self.Notification_send(message)
        except IndexError:
            print("エラー！引数に不正があります")
        
    def Visualization_send(self,image_path,text):
        try:
            files = {'file': open(image_path, 'rb')}
            print("visualization send!")
            #画像ファイルを送信
            url = "https://slack.com/api/files.upload"
            data = {
                "token": self.token,
                "channels": self.channels,
                "title": "test file",
                "initial_comment": text
              }
            requests.post(url, data=data, files=files)
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]

    def Visualization_Sitting(self,path):
        array = np.loadtxt(path)
        print(array)
        size = array.shape[0]
        #blue
        col1 = np.array([0.0,156/255,209/255])
        #yellow
        col2 = np.array([255/255,217/255,0.0])
        #label
        st = ["Standing","Sitting"]
        colorlist = np.zeros((size,3),np.float64)
        label_list = []
        #create label and color list
        for w in range(size):
            if array[w,1] == 0:
                colorlist[w,:] = col1[:]
                label_list.append(st[0])
            else:
                colorlist[w,:] = col2[:]
                label_list.append(st[1])
        #create Graph
        plt.figure()
        plt.pie(array[:,0], labels=label_list,colors = colorlist,startangle=90,counterclock=False)
        label_time = ["AM","PM"]
        x_time = np.array([100 , 100])
        colorlist_time = ["pink","magenta"]
        plt.pie(x_time, labels=label_time,colors = colorlist_time,startangle=90,counterclock=False,radius = 0.7,labeldistance=0.5)
        centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        print("Sitting Graph created!")
        #save graph
        file_path = "Sitting_Graph.png"
        fig.savefig(file_path)
        message = "昨日1日のあなたの座っていた時間の記録のグラフです！"
        self.Visualization_send(file_path,message)

    def Visualization_Ventilation(self,path):
        array = np.loadtxt(path)
        size = array.shape[0]
        #green
        col1 = np.array([176/255,255/255,5/255])
        #yellow
        col2 = np.array([23/255,152/255,251/255])
        #label
        st = ["Close","Open"]
        colorlist = np.zeros((size,3),np.float64)
        label_list = []
        #create label and color list
        for w in range(size):
            if array[w,1] == 0:
                colorlist[w,:] = col1[:]
                label_list.append(st[0])
            else:
                colorlist[w,:] = col2[:]
                label_list.append(st[1])
        #create Graph
        plt.figure()
        plt.pie(array[:,0], labels=label_list,colors = colorlist,startangle=90,counterclock=False)
        label_time = ["AM","PM"]
        x_time = np.array([100 , 100])
        colorlist_time = ["pink","magenta"]
        plt.pie(x_time, labels=label_time,colors = colorlist_time,startangle=90,counterclock=False,radius = 0.7,labeldistance=0.5)
        centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        print("Ventilation Graph created!")
        #save graph
        file_path = "Ventilation_Graph.png"
        fig.savefig(file_path)
        message = "昨日1日のあなたの家の窓の開閉の記録のグラフです！"
        self.Visualization_send(file_path,message)

    def Visualization_HeatStroke(self,path):
        df = pd.read_csv(path,parse_dates=[0])
        # グラフ作成
        plt.figure(figsize=(8,4))
        plt.plot(pd.to_datetime(df['date']), df['Temp'],color = "red",marker='D')
        plt.plot(pd.to_datetime(df['date']), df['Hum'],color = "cyan",marker = 'o')
        plt.plot(pd.to_datetime(df['date']), df['WBGT'],color = "black",marker='*')
        plt.legend(['Temp','Humidity','WBGT'])
        # ロケータで刻み幅を設定
        xloc = mpl.dates.HourLocator(byhour=range(0,24,3))
        plt.gca().xaxis.set_major_locator(xloc)
        # 時刻のフォーマットを設定
        xfmt = mpl.dates.DateFormatter("%H:%M")
        plt.gca().xaxis.set_major_formatter(xfmt)
        print("HeatStroke Graph created!")
        #save graph
        file_path = "HeatStroke_Graph.png"
        plt.savefig(file_path)
        message = "昨日1日のあなたの家の気温、湿度、WBGTのグラフです！"
        self.Visualization_send(file_path,message)



        
