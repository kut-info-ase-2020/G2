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
import matplotlib.patches as mpatches
from PIL import Image
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
            message = "You're sitting in your chair too much! Stand up out of your chair and try some light exercise!\nSitting time is " + str(time) + " minute."
            self.Notification_send(message)
        except IndexError:
            print("Error! Bad argument.")
    def Notification_Ventilation(self,time):
        try:
            print("Ventilate notification message create...")
            message = "It hasn't been ventilated in a while! Open a window and try to ventilate it!\nclosing window time is " + str(time) + " minute."
            self.Notification_send(message)
        except IndexError:
            print("Error! Bad argument.")

    def Notification_HeatStroke(self,Temp,Hum):
        try:
            print("Heatstroke notification message create...")
            message = "Warning: You have a high risk of heat stroke!\nHow to avoid heat stroke: use fans or air conditioners, drink plenty of water, etc.\nsee:https://www.city.minato.tokyo.jp/kuse/koho/minatomonthly/170601/heat-stroke-prevention.html\nTemprerature is "+ str(Temp) + ".\nHumidity is " + str(Hum) + "."
            self.Notification_send(message)
        except IndexError:
            print("Error! Bad argument.")
        
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
        array_pl = np.loadtxt(path,delimiter=',')
        print(array_pl.shape)
        print(array_pl)
        array = array_pl.reshape((-1, 2))
        print(array.shape)
        print(array)
        #final  = np.zeros((1,2),np.float64)
        #final[0,:] = [2358,0]
        #print(final.shape)


        #array = np.insert(array,array.shape[0]-1,[2359,1],axis=0)
        #array = np.concatenate([array,final],0)
        #array  = np.append(array,final,axis = 0)
        #print(array)
        size = array.shape[0]
        #blue
        col1 = np.array([0.0,156/255,209/255])
        #yellow
        col2 = np.array([255/255,217/255,0.0])
        #label
        st = ["Standing","Sitting"]
        colorlist = np.zeros((size+1,3),np.float64)
        #start_time = int(array[0,0])
        now_time = 0
        time_array = [] 
        label_list = ['Standing']
        #create label and color list
        for w in range(size+1):
            if w == size:
                time_array.append(2398 - now_time)
                colorlist[w,:] =  col1[:]
                label_list.append(st[0])

                #time_array.append(1)
                #colorlist[w+1,:] =  col1[:]
                #label_list.append(st[0])
                break
            num = int(array[w,0])
            minute = num %100
            hour = (num - minute)
            print(minute)
            print(hour)
            minute = round(minute*1.6666666666666666)
            num = hour + minute
            sabun_time = num - now_time
            now_time = num
            print(now_time)
            time_array.append(sabun_time)
            
            if array[w,1] == 0:
                colorlist[w,:] = col1[:]
                label_list.append(st[0])
            else:
                colorlist[w,:] = col2[:]
                label_list.append(st[1])
        #create Graph
        print(time_array)
        #print(time_array.shape)
        print(colorlist)
        print(label_list)
        plt.figure()
        plt.pie(time_array,colors = colorlist,startangle=90,counterclock=False)
        label_time = ["AM","PM"]
        x_time = np.array([100 , 100])
        print(col1)
        colorlist_time = ["pink","magenta"]
        plt.pie(x_time, labels=label_time,colors = colorlist_time,startangle=90,counterclock=False,radius = 0.7,labeldistance=0.5)
        centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        patch_list = []
        patch_list.append(mpatches.Patch(color=col1,label = st[0]))
        patch_list.append(mpatches.Patch(color=col2,label = st[1]))
        plt.legend(st,bbox_to_anchor=(1.3, 1.1), loc='upper right', handles = patch_list,borderaxespad=0, fontsize=15)
        print("Sitting Graph created!")
        #save graph
        file_path = "Sitting_Graph.png"
        fig.savefig(file_path)
        
        img = np.array(Image.open('SlackAPI/tokei.png'))
        graph = np.array(Image.open(file_path))
        new_graph = np.where(img == [255, 255, 255, 255], graph, img)
        pil_img = Image.fromarray(new_graph)
        #print(pil_img.mode) #RGBA
        pil_img.save(file_path)
        message = "Here's a graph of your sitting time at yesterday!"
        self.Visualization_send(file_path,message)

    def Visualization_Ventilation(self,path):
        array_pl = np.loadtxt(path,delimiter=',')
        print(array_pl.shape)
        print(array_pl)
        array = array_pl.reshape((-1, 2))
        print(array.shape)
        print(array)
        size = array.shape[0]
        #green
        col1 = np.array([176/255,255/255,5/255])
        #yellow
        col2 = np.array([23/255,152/255,251/255])
        #label
        st = ["Close","Open"]
        colorlist = np.zeros((size,3),np.float64)
        #start_time = int(array[0,0])
        now_time = 0
        time_array = []
        label_list = ['Close']
        #create label and color list
        for w in range(size+1):
            if w == size:
                time_array.append(2398 - now_time)
                label_list.append(st[0])
                break
            num = int(array[w,0])
            minute = num %100
            hour = (num - minute)
            print(minute)
            print(hour)
            minute = round(minute*1.6666666666666666)
            num = hour + minute
            sabun_time = num - now_time
            now_time = num
            print(now_time)
            time_array.append(sabun_time)
            
            if array[w,1] == 0:
                colorlist[w,:] = col1[:]
                label_list.append(st[0])
            else:
                colorlist[w,:] = col2[:]
                label_list.append(st[1])
        #create Graph
        print(time_array)
        print(label_list)
        plt.figure()
        plt.pie(time_array, colors = colorlist,startangle=90,counterclock=False)
        label_time = ["AM","PM"]
        x_time = np.array([100 , 100])
        colorlist_time = ["pink","magenta"]
        plt.pie(x_time, labels=label_time,colors = colorlist_time,startangle=90,counterclock=False,radius = 0.7,labeldistance=0.5)
        centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        patch_list = []
        patch_list.append(mpatches.Patch(color=col1,label = st[0]))
        patch_list.append(mpatches.Patch(color=col2,label = st[1]))
        plt.legend(st,bbox_to_anchor=(1.3, 1.1), loc='upper right', handles = patch_list,borderaxespad=0, fontsize=15)
        print("Ventilation Graph created!")
        #save graph
        file_path = "Ventilation_Graph.png"
        fig.savefig(file_path)
        
        img = np.array(Image.open('SlackAPI/tokei.png'))
        graph = np.array(Image.open(file_path))
        new_graph = np.where(img == [255, 255, 255, 255], graph, img)
        pil_img = Image.fromarray(new_graph)
        #print(pil_img.mode) #RGBA
        pil_img.save(file_path)
        
        message = "Here's a graph of your house's window openings and closings at yesterday!"
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
        message = "Here's a graph of your home's temperature, humidity and WBGT at yesterday!"
        self.Visualization_send(file_path,message)



        
