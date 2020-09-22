# 換気システム（センサー部）

換気システムのうち，センサーの値の取得から通知・データの送信までを担当する．

## ファイル構成

- ventilation_system.py
    - メイン関数があるファイル
    - 各種機能の呼び出しを行う
- windowtimer.py
    - 定期的な実行を担う関数があるファイル
    - 日替わり時の関数呼び出し，定期的なセンサー値の取得，長時間窓が閉まっているときの関数呼び出しなど
- reedswitch.py
    - 実際にセンサーを扱う関数があるファイル
    - RPi.GPIOのラッパ的なもの
- sensor.py
    - センサー全般の親クラスを意識して作ったけど正直いらないかも
    - reedswitchが継承している

## 作成した関数と仕様

- selfは省略
- ventilation_system.py
    - VentilationSystemクラス
        - setup()
            - 最初に呼び出すやつ
            - initで呼ばれるのでそんなに意識しなくて良い
            - periodical_reportやwarningなどのコールバック関数をWindowTimerにセットしたり，天気APIクラス等の外部クラスをインスタンス化する
        - start()
            - 実際に動作を開始する
        - periodical_report(csv_data_path)
            - 定時に呼び出される関数
            - Visualization用関数を呼ぶ
        - warning(hour, minutes)
            - 長時間窓がしまっているときに呼び出される関数
            - Slackを通じた通知を行う
        - resolved()
            - 窓が開いたときに通知するとかいう話があった気がした
            - とりあえず今は何もしないようにしている
        - print_debug()
            - デバッグ用表示関数
            - ちゃんとコールバック関数がセットされているか表示するだけ
- windowtimer.py
    - WindowOpeningTimerクラス
        - no_use_func()
            - 何もしない関数
            - デフォルトでコールバック関数として入れておく
        - start()
            - 使用するリードスイッチを初期化し，タイマーの動作を開始する
        - destroy()
            - タイマーの設定をリセットする
        - timer_loop()
            - タイマーのメインループ
            - 30分ごとの測定の管理と定時報告用コールバック関数の呼び出しを行う
        - measurement_next()
            - 30分に1回呼び出される，窓が開いているかどうかの判定結果を元にコールバック関数を呼び出す関数
            - 長時間閉まっていた場合，窓が開いた場合
        - get_window_status()
            - センサーから実際に値を取ってきて，窓の状態を判定する関数
            - 1分間1秒ごとに値を取得，その後取った値の平均を計算する
            - 四捨五入した結果開いているかどうかを判定する
            - 計測を開始した時刻とWindowData（計測を開始した時刻の文字列表現，判定結果）のタプルを返す
        - write_csv(filename, data)
            - filenameというcsvファイルにdataの中身を書く関数
            - csvファイルへの保存
        - read_next(sensor, res_list)
            - sensorから読み出した値をres_listに格納する
        - その他セッター等
- reedswitch.py
    - ReedSwitchクラス
        - setup(port)
            - 初期化関数．initで呼ばれる
            - portで指定したピンにデータが入ってくるようにすること
        - read()
            - 値の読み出し
            - 磁力が強いとき1を返す
        - main()
            - テスト用
- sensor.py
    - UninitializedErrorクラス
        - 初期化前に値を読み出そうとしたときなどに投げるエラー
    - Sensorクラス
        - setup(ports, port_settings, port_mode)
            - 初期化
            - portsに使用するポート，port_settingsに同順でINPUTかOUTPUTかをそれぞれリストで放り込む
            - port_modeはBCMで指定するかBOARDで指定するか．デフォルトはBCM
        - read(port)
            - portから値を読み出す．INPUTモードになってなかったり未初期化ならエラー
        - write(port, value)
            - portにvalueを書き込む．OUTPUTモードになってなかったり未初期化ならエラー
