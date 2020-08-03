# 換気機能で用いるWeatherAPI
## 試すAPI

### Open WeatherAPI

無料枠　100リクエスト/日

地名，経度・緯度で位置指定可能

## 環境
ubuntu 18.04

python 3.6

Dockerfileを参照 

## Docker用コマンド
docker built -t ubuntu_python

docker run -it -v $(pwd):/workspace ubuntu_python
