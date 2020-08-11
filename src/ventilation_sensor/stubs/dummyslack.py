from sys import stderr
class Slack:
    def send_report(self, path):
        print("dummy slack: sending report...", file=stderr)
        print("path: " + path, file=stderr)
        print(path)
    def send_notification(self, message):
        print("dummy slack: sending message...", file=stderr)
        print("message: " + message, file=stderr)
        print(message)
