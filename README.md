# G2 「Smart Remotework Assistant」

## 使用言語
Python3.6

## 主な使用ライブラリ
sched, datetime, matplotlib, SlackClient, json, requests

## 各システムの簡単な説明
以下の起動コマンドはカレントディレクトリをsrcディレクトリとした場合の記述である  
またSlackとの連携にはSlack Appの登録と`bot`、`channels:history`、`chat:write:bot`の3つのスコープを持ったAPI keyが必要となる。


### Sitting time management
連続して座った時間を計測し、基準の時間を超えるとSlackで警告を出すシステム  
また、日付が変わると１日の座った時間の遷移を示すグラフをSlackに出力する

#### 主な利用ファイル
sitting_time_sensor/sitting_time_system.py システムの呼び出し  
sitting_time_sensor/sittingtimer.py　システムのスケジューリング、座った時間の計測と記録  
SlackAPI/SlackAPI_class.py　警告とグラフの出力  

#### 起動コマンド
`python3 -m sitting_time_sensor/sitting_time_system`

### Weather-wise ventilation management
連続して換気されていない時間を計測し、基準の時間を超えるとSlackで警告を出すシステム  
また、日付が変わると１日の窓の状態の遷移を示すグラフをSlackに出力する

#### 主な利用ファイル
ventilation_sensor/ventilation_system.py システムの呼び出し  
ventilation_sensor/windowtimer.py　システムのスケジューリング、密閉時間の計測と記録  
weatherAPI/weather.py　Weather APIによる天気情報の取得(実行にはOpen Weather APIのAPI keyの取得が必要)  
SlackAPI/SlackAPI_class.py　警告とグラフの出力  

#### 起動コマンド
`python3 -m ventilation_sensor/ventilation_system`

### Heatstroke risk forecast
部屋の気温・湿度から求める熱中症の危険度を示すWBGTが基準値を超えるとSlackで警告を出すシステム  
また、日付が変わると１日の気温、湿度、WBGTの遷移を表すグラフをSlackに出力する

#### 主な利用ファイル
calWBGT.py WBGTの計測と記録
scheduler_WBGT.py システムの呼び出しとスケジューリング

#### 起動コマンド
`python3 scheduler_WBGT.py`

### Slack BOT
Slack内で警告やチャットでの設定変更などを行うシステム  
Real Time Messaging APIを利用している為、このサイト(https://api.slack.com/rtm)で紹介される古いバージョンの権限を持ったAPI keyが必要
また位置情報として利用可能な地名はOpen Weather Map(https://openweathermap.org/)で登録された地名を用いる

#### 主な利用ファイル
bot_run.py　Botの起動

#### 起動コマンド
`python3 bot_run.py`
