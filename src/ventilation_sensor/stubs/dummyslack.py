from sys import stderr
class Slack:
    def Visualization_Ventilation(self, path):
        print("dummy slack: sending report...", file=stderr)
        print("path: " + path, file=stderr)
        print(path)
    def Notification_Ventilation(self, minutes):
        print("dummy slack: sending notification...", file=stderr)
        print("minutes: " + str(minutes), file=stderr)
        print(minutes)
    def __init__(self, token, channel):
        pass
