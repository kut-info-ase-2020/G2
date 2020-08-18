import numpy as np
import matplotlib.pyplot as plt


# 円グラフを描画
x = np.array([1000, 150, 250 ,350 , 200 ,50, 400])
col1 = "cyan"
col2 = "yellow"
colorlist = [col1,col2,col1 , col2 , col1 , col2 , col1]
st = ["Standing","Sitting"]

print("Graph creating...")
label = [st[0],st[1],st[0], st[1], st[0], st[1], st[0]]
plt.pie(x, labels=label,colors = colorlist,startangle=90,counterclock=False,explode=[0,0.05,0,0.05,0,0.05,0])

label_time = ["AM","PM"]
x_time = np.array([100 , 100])
colorlist_time = ["pink","magenta"]
plt.pie(x_time, labels=label_time,colors = colorlist_time,startangle=90,counterclock=False,radius = 0.7,labeldistance=0.5)

centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
print("Graph created!")
fig.savefig("Sitting_Graph.png")


plt.figure(figsize=(8,4))
plt.plot(df['date'], df['Temp'],color = "red",marker='D')
plt.plot(df['date'], df['Hum'],color = "cyan",marker = 'o')
plt.plot(df['date'], df['WBGT'],color = "black",marker='*')
plt.legend(['Temp','Humidity','WBGT'])
# ロケータで刻み幅を設定
xloc = mpl.dates.HourLocator(byhour=range(0,24,1))
plt.gca().xaxis.set_major_locator(xloc)
# 時刻のフォーマットを設定
xfmt = mpl.dates.DateFormatter("%H")
plt.gca().xaxis.set_major_formatter(xfmt)
print("HeatStroke Graph created!")
#save graph
file_path = "HeatStroke_Graph.png"
fig.savefig(file_path)
message = "昨日1日のあなたの家の気温、湿度、WBGTのグラフです！"
self.Visualization_send(file_path,message)
