
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hieupro.helpers.MailMan import MailMan
from hieupro.controller.sso_controller import SSOController

app = Flask(__name__)
mail_man = MailMan()


def mock_get_sso_info(payload):
    domain = '127.0.0.1'
    secret_key = payload['secret_key']
    username = payload['username']
    res = SSOController.get_sso_information(domain=domain, secret_key=secret_key, username=username)
    if res:
        return res
    return None


def init_api(my_app):
    global app
    app = my_app
    global mail_man
    mail_man = MailMan(app)

    @app.route('/sso/register', methods=['POST'])
    @jwt_required
    def sso_register():
        username = get_jwt_identity()['username']
        if request.get_json():
            payload = request.get_json()
            domain = payload['domain']
            ok = SSOController.sso_register(mailman=mail_man, username=username, domain=domain)
            if ok:
                return jsonify(code='success', msg='your domain register success')
        return jsonify(code='fail', msg='your domain already exists')

    @app.route('/sso/get_info', methods=['POST'])
    def get_sso_info():
        domain = request.remote_addr
        payload = request.get_json()['query_data']
        secret_key = payload['secret_key']
        username = payload['username']
        res = SSOController.get_sso_information(domain=domain, secret_key=secret_key, username=username)
        if res:
            return jsonify(res)
        return jsonify({})

    @app.route('/sso/my_domains')
    @jwt_required
    def get_my_domains():
        username = get_jwt_identity()['username']
        return jsonify(SSOController.get_my_domains(username))

