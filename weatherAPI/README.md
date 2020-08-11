# 換気機能で用いるWeatherAPIによる天気の判定を行うクラス
換気通知機能に用いる天気の判定を行うWeatherクラス(weather.py)
API Keyは環境変数weatherapi_keyに設定する

#### 他プログラムの用途
Requestsライブラリのテスト request_test.py

APIのテスト weatherAPI_test.py

Weatherクラスの動作テスト test_weather.py

Weatherクラスの単体テスト unittest_weather.py

## 使用API

### Open WeatherAPI

無料枠　100リクエスト/日

地名，経度・緯度で位置指定可能

## 環境
ubuntu 18.04

python 3.6

Dockerfileを参照 

## Docker用コマンド
**イメージの作成**

`docker built -t ubuntu_python`

**コンテナの起動** カレントディレクトリをマウントする

`docker run -it -v $(pwd):/workspace --name weatherapi ubuntu_python`

**起動中コンテナ(weatherapi)のターミナルにアクセス**

`docker attach weatherapi`
