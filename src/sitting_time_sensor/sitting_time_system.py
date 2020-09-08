import os
from sys import stderr
from sitting_time_sensor.sittingtimer import SittingTimer
# from SlackAPI.SlackAPI_class import SlackAPI
# from sitting_time_sensor.stubs.dummytimer import SittingTimer
from sitting_time_sensor.stubs.dummyslack import SlackAPI

class SittingTimeSystem:
    """SittingTimeSystem
    """
    timer = None
    ui = None
    def setup(self):
        SittingTimeSystem.timer = SittingTimer()
        slack_token = os.environ['SLACK_API_TOKEN']
        slack_channnel = '#zikkenzyou_go'
        SittingTimeSystem.ui = SlackAPI(slack_token, slack_channnel)
        SittingTimeSystem.timer.set_time_over_callback(interval=30, func=self.warning)
        SittingTimeSystem.timer.set_stand_callback(func=self.resolved)
        SittingTimeSystem.timer.set_period_callback(func=self.periodical_report)

    def start(self):
        SittingTimeSystem.timer.start()
    
    def periodical_report(self, csv_data_path):
        if os.path.exists(csv_data_path):
            SittingTimeSystem.ui.Visualization_Sitting(csv_data_path)
        else:
            print("Sitting Time System Warning: " + csv_data_path + " don't exists!")

    def warning(self, hour, minutes):
        sitting_minutes = int(hour) * 60 + int(minutes)
        SittingTimeSystem.ui.Notification_Sitting(sitting_minutes)

    def resolved(self):
        pass
        # SittingTimeSystem.ui.send_notification(message)

    def print_debug(self):
        pass

    def __init__(self):
        self.setup()

if __name__ == "__main__":
    vs = SittingTimeSystem()
    vs.start()
