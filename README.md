# G2
以下のサイトを利用し、気温と湿度から室内のWBGTを計測しています。室内を想定しています。  
https://ameblo.jp/bokunimo/entry-12497181208.html  
https://www.wbgt.env.go.jp/wbgt_data.php

使用ライブラリ  
import csv  
from datetime import datetime, timedelta, timezone  
import statistics  

関数「calWBGT()」の仕様   
+この関数を呼び出すと、以下のことが起きます  
  +「dataWBGT.csv」に関数呼び出した時のデータが追加で格納  
  +WBGT値が危険な場合、返り値として「１」が返ってくる。  
+データは複数回センサーの値を取り出し、その中央値を選んでいます  
  +初期設定は10回です  
+故障時には一定の回数センシングを行った後、以下のことが起きます  
  +「dataWBGT.csv」に時間以外のデータを「－１」で格納  
  +0WBGT値が危険な場合、返り値として「－１」が返ってくる。  
