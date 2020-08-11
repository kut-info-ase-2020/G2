from sys import stderr
class WindowOpeningTimer:
    def set_window_open_callback(self, func):
        self.open_callback = func
    def set_midnight_callback(self, func):
        self.midnight_callback = func
    def show_window_open_callback():
        print("window_open_callback:" + str(self.open_callback), file=stderr)
    def show_midnight_callback():
        print("midnight_callback:" + str(self.midnight_callback), file=stderr)
    def call_window_open_callback(self, file_path):
        self.open_callback(file_path)
    def call_midnight_callback(self, hour, minutes):
        self.open_callback(hour, minutes)
    def start(self):
        print("dummy timer: started", file=stderr)
