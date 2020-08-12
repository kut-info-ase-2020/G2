import os
# from windowtimer import WindowOpeningTimer
# from weatherinfo import Weatherinfo
# from slackcommunicator import SlackNotification, SlackReport
from stubs.dummytimer import WindowOpeningTimer
from stubs.dummyweather import Weatherinfo
from stubs.dummyslack import Slack

class VentilationSystem:
    """VentilationSystem
    """
    timer = None
    weather = None
    ui = None
    def setup(self):
        VentilationSystem.timer = WindowOpeningTimer()
        VentilationSystem.weather = Weatherinfo()
        VentilationSystem.ui = Slack()
        VentilationSystem.timer.set_time_over_callback(interval=30, func=self.warning)
        VentilationSystem.timer.set_window_open_callback(func=self.resolved)
        VentilationSystem.timer.set_period_callback(func=self.periodical_report)
        VentilationSystem.timer.start()
    
    def periodical_report(self, csv_data_path):
        if os.path.exists(csv_data_path):
            VentilationSystem.ui.send_report(csv_data_path)
        else:
            print("Ventilation System Warning: " + csv_data_path + " don't exists!")

    def warning(self, hour, minutes):
        today = VentilationSystem.weather.get_today()
        if today == 'sunny' or today == 'cloudy':
            message = "Warning: sitting for long periods (" + str(hour) + " hr. " + str(minutes) + " min.)"
            VentilationSystem.ui.send_notification(message)

    def resolved(self):
        message = "Notification: window opened!"
        VentilationSystem.ui.send_notification(message)

    def print_debug(self):
        VentilationSystem.timer.show_window_open_callback()
        VentilationSystem.timer.show_midnight_callback()

    def __init__(self):
        self.setup()

if __name__ == "__main__":
    VentilationSystem()
