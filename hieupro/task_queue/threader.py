from threading import Thread
from hieupro.constants.constants import ACTION_SEND_MAIL


class MyThread(Thread):
    def __init__(self, command, app, *argv):
        super(MyThread, self).__init__()
        self.name = command
        self.app = app
        self.args = argv

    def run(self):
        switchers = {
            ACTION_SEND_MAIL: send_mail(self.app, self.args[0], self.args[1], self.args[2], self.args[3])
        }
        x = switchers[self.name]


def send_mail(app, mailman, title, content, receiver):
    with app.app_context():
        mailman.send_mail(title=title,
                          content=content,
                          receiver=receiver)
    return True
