from sys import stderr
class WindowOpeningTimer:
    def set_time_over_callback(self, interval, func):
        self.interval = interval
        self.time_over_callback = func
    def set_window_open_callback(self, func):
        self.open_callback = func
    def set_period_callback(self, func):
        self.period_callback = func
    def show_window_open_callback():
        print("window_open_callback:" + str(self.open_callback), file=stderr)
    def show_period_callback():
        print("period_callback:" + str(self.midnight_callback), file=stderr)
    def call_window_open_callback(self, file_path):
        self.open_callback(file_path)
    def call_period_callback(self, hour, minutes):
        self.open_callback(hour, minutes)
    def start(self):
        print("dummy timer: started", file=stderr)
