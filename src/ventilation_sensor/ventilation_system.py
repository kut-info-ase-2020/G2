import os
# from windowtimer import WindowOpeningTimer
from weatherAPI.weather import Weather
# from slackcommunicator import SlackNotification, SlackReport
from ventilation_sensor.stubs.dummytimer import WindowOpeningTimer
# from ventilation_sensor.stubs.dummyweather import Weather
from ventilation_sensor.stubs.dummyslack import Slack

class VentilationSystem:
    """VentilationSystem
    """
    timer = None
    weather = None
    ui = None
    def setup(self):
        VentilationSystem.timer = WindowOpeningTimer()
        VentilationSystem.weather = Weather()
        slack_token = os.environ['SLACK_API_TOKEN']
        slack_channnel = '#zikkenzyou_go'
        VentilationSystem.ui = Slack(slack_token, slack_channnel)
        VentilationSystem.timer.set_time_over_callback(interval=30, func=self.warning)
        VentilationSystem.timer.set_window_open_callback(func=self.resolved)
        VentilationSystem.timer.set_period_callback(func=self.periodical_report)

    def start(self):
        VentilationSystem.timer.start()
    
    def periodical_report(self, csv_data_path):
        if os.path.exists(csv_data_path):
            VentilationSystem.ui.Visualization_Ventilation(csv_data_path)
        else:
            print("Ventilation System Warning: " + csv_data_path + " don't exists!")

    def warning(self, hour, minutes):
        if not VentilationSystem.weather.is_rainy():
            # message = "Warning: sitting for long periods (" + str(hour) + " hr. " + str(minutes) + " min.)"
            close_minutes = int(hour) * 60 + int(minutes)
            VentilationSystem.ui.Notification_Ventilation(close_minutes)

    def resolved(self):
        pass
        # message = "Notification: window opened!"
        # VentilationSystem.ui.send_notification(message)

    def print_debug(self):
        VentilationSystem.timer.show_window_open_callback()
        VentilationSystem.timer.show_midnight_callback()

    def __init__(self):
        self.setup()

if __name__ == "__main__":
    vs = VentilationSystem()
    vs.start()
