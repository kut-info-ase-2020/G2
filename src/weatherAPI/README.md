# 換気機能で用いるWeatherAPIによる天気の判定を行うクラス
換気通知機能に用いる天気の判定を行うWeatherクラス(weather.py)
API Keyは環境変数weatherapi_keyに設定する
#### weatherAPIの関数の説明
get_weather 
- 現在の天気を取得する関数
- 引数なし，返り値:現在の天気(Clouds, Rainなど)

is_raining
- 今の天気が雨(Rain)かどうか調べる関数
- 引数なし，返り値:True，Flase

set_placename
- 天気の情報を取得する際に利用する地名を設定する関数
- 引数: place_name(入力形式: City name,Country 例: Kochi,jp)
- 返り値: 変更されたかを表す文字列

set_location
- 天気の情報を取得する際に利用する経度，緯度の位置情報を設定する関数
- 引数: lon,lat #経度,経度を表す数値の入力
- 返り値: 変更されたかを表す文字列

change_mode
- 天気の情報を地名で取得するか，経度緯度で取得するかを変更する関数
- 引数: mode_name(入力形式: 文字列(地名: PlaceName，経度緯度: Location)
- 返り値: 変更が行われたかを表す文字列

get_placenamme
- 現在設定されている地名を取得する関数
- 引数: なし，返り値: 設定されている地名の文字列

get_location
- 現在設定されている経度緯度の値を取得する関数
- 引数: なし，返り値: 設定されている経度緯度の値

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
