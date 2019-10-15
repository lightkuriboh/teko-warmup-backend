
from flask_mail import Mail
from flask_mail import Message
from config import MailConfig


class MailMan:

    def __init__(self, app=None):
        if app:
            app.config['MAIL_SERVER'] = MailConfig.MAIL_SERVER
            app.config['MAIL_PORT'] = MailConfig.MAIL_PORT
            app.config['MAIL_USERNAME'] = MailConfig.MAIL_USERNAME
            app.config['MAIL_PASSWORD'] = MailConfig.MAIL_PASSWORD
            app.config['MAIL_USE_TLS'] = MailConfig.MAIL_USE_TLS
            app.config['MAIL_USE_SSL'] = MailConfig.MAIL_USE_SSL
            self.mail = Mail(app)

    def send_mail(self, title, content, receiver):
        msg = Message(title,
                      sender=MailConfig.MAIL_USERNAME,
                      recipients=[receiver])
        msg.body = content
        self.mail.send(msg)
