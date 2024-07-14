import atexit
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, request, jsonify, send_from_directory
from flask_restx import Api, Resource, fields
from flask_mail import Mail, Message

from db_conn import Session
from nws_models import User
from nws_service import UserService, NewsletterService

# ---------------- Newsletter App ----------------
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configuração de e-mail (substitua com suas próprias configurações em .env)
MAIL_SERVER = app.config['MAIL_SERVER']
MAIL_PORT = app.config['MAIL_PORT']
MAIL_USE_TLS = app.config['MAIL_USE_TLS']
MAIL_USERNAME = app.config['MAIL_USERNAME']
MAIL_PASSWORD = app.config['MAIL_PASSWORD']

mail = Mail(app)
user_service = UserService(mail)

api = Api(app, version='1.4', title='Notification Service API',
          description='A simple Notification Service API')

ns = api.namespace('newsletter', description='Serviço de entrega de informativos climáticos.')

# ---------------- Modelagem dos dados para o Swagger ----------------

user_model = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'frequency': fields.String(required=True, description='Notification frequency', enum=['minute', 'daily', 'weekly', 'biweekly', 'monthly', 'semiannual'])
})

# ------------ Endpoints ------------
"""
    Serviço de Cadastro e Descadastro de Usuários
""" 

@app.route('/home')
def index():
    return send_from_directory(directory='templates', path='index.html')

# Registro de usuário
@ns.route('/register')
class Register(Resource):

    @ns.expect(user_model)
    @ns.response(201, 'Usuário registrado com sucesso!')
    @ns.response(400, 'Invalid input')
    def post(self):
        
        data = request.get_json()
        email = data.get('email')
        frequency = data.get('frequency')

        if not email or frequency not in ['minute', 'daily', 'weekly', 'biweekly', 'monthly', 'semiannual']:
            return {"error": "Invalid input"}, 400

        user = user_service.register_user(email, frequency)
        return {"message": "Usuário registrado com sucesso!", "user": user.email}, 201

# Descadastro de usuário
@ns.route('/unsubscribe')
class Unsubscribe(Resource):
    
    @ns.param('email', 'The user email')
    @ns.response(200, 'Usuário descadastrádo com sucesso.')
    @ns.response(400, 'Invalid input')
    def delete(self):
        email = request.args.get('email')

        if not email:
            return {"error": "Invalid input"}, 400

        success = user_service.unsubscribe_user(email)
        if success:
            return {"message": "Usuário descadastrádo com sucesso."}, 200
        return {"error": "User not found"}, 404

"""
    Serviço de Envio de emails aos usuários
""" 
@ns.route('/send_email')
class SendEmail(Resource):
    
    @ns.response(200, 'Emails enviados com sucesso!')
    @ns.response(500, 'Failed to send emails')
    def post(self):

        try:
            # ---------- Log do tempo de execução ----------
            # TODO: imprima a execução dos últimos 5 envios.
            # ---------- Agendamento dos Emails ----------
            app.logger.info("Iniciando o envio de emails...")
            
            # Criando uma instância de NewsletterService com o objeto de e-mail configurado
            newsletter_service = NewsletterService(mail=app.config['MAIL_USERNAME'])
            newsletter_service.initialize_mail(mail)

            # Envia os e-mails imediatamente para os usuários que precisam receber agora
            newsletter_service.send_notifications()

            return {"message": "Emails enviados com sucesso!"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == '__main__':
    
    # --------------- Agendamento de Emails --------------- 
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=newsletter_service.send_notifications, trigger='interval', minutes=1)
    scheduler.start()

    # Para garantir que o scheduler é parado quando a aplicação é encerrada
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=True, port=5003)
