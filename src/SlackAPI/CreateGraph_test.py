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