
from flask import Flask, render_template
from flask_jwt_extended import decode_token
from hieupro.controller.confirmation_controller import ConfirmationController
from hieupro.helpers.MailMan import MailMan
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.TokenServices import TokenManager

app = Flask(__name__)
mail_man = MailMan()


def init_api(my_app):
    global app
    app = my_app
    global mail_man
    mail_man = MailMan(app)

    @app.route('/confirm/register/<path:token>')
    def confirm_register(token):
        payload = decode_token(token)
        if TokenManager.token_expired(payload):
            return render_template('register_confirmation.html', message="Your session expired, Please register again!")
        success = ConfirmationController.confirm_register(payload['identity'])
        if success:
            return render_template('register_confirmation.html', message="You registered successfully!")
        return render_template('register_confirmation.html', message="Your email or username is duplicated!")

    @app.route('/confirm/password_reset/<path:token>')
    def confirm_password_reset(token):
        payload = decode_token(token)
        if TokenManager.token_expired(payload):
            return render_template('register_confirmation.html',
                                   message="Your session expired, Please reset your password again!")
        success = ConfirmationController.confirm_password_reset(payload['identity'])
        if success:
            return render_template('register_confirmation.html', message="Your password reset successfully!")
        return render_template('register_confirmation.html', message="You reset password already!")
