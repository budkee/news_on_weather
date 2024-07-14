import atexit
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from flask_mail import Message, Mail
from nws_models import User, EmailLog
from db_conn import Session
from config import DATABASE_URI, MAIL_USERNAME

class UserService():

    def __init__(self, mail):
        # Para envio de emails
        self.mail = mail
        # Para envio de dados ao bd
        self.db = Session()

    # -------- Comunicação com o newsletter_db --------
    def register_user(self, email, frequency):
        
        user = User(email=email, frequency=frequency)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def unsubscribe_user(self, email):
        
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_all_users(self):
        return self.db.query(User).all()


class NewsletterService():
    
    def __init__(self, mail):
        # Para envio de emails
        self.mail = None
        # Para envio de dados ao bd
        self.db = Session()

    # Método para inicializar o objeto Mail
    def initialize_mail(self, mail):
        self.mail = mail  

    # Recuperar os usuários inscritos e seus períodos de preferência
    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()
    
    # -------- Comunicação com a API interna --------
    # 1. Recuperar os dados das condições climáticas
    def get_weather_data_from_api(self):
        """
            Extração do DataService(ETL)

            # 1. Pegar os dados da API do DataService: http://127.0.0.1:5002/weather/data e retornar o JSON.

        """
        try:

            endpoint_ufms = "http://localhost:6767/weather/latest_data"
            response = requests.get(endpoint_ufms)
            response.raise_for_status()
            weather_data = response.json()
            
            # Retorna os dados climáticos do dia
            return weather_data

        except Exception as e:
            print(f"Não foi possível coletar os dados da API: {str(e)}")
            return None
    
    # 2. Formatar os dados o boletim
    def formatar_boletim(self, weather_data_json):
        """
            Recebe os dados coletados pela WeatherService API, formata o relatório e retorna uma lista com todos os reports.

            Quando será executado?
            - Ao finalizar a extração dos dados da API.

        """
        try:
            """
                Área de Staging de dados vindos da API interna (DataService API).

                Entrada: JSON contendo a previsão do tempo atual.
                Saída: Lista com todos os reports
            """
            # Lista para armazenar os boletins que já foram formatados
            weather_reports = [] 

            # Coleta dos dados da WeatherAPI
            for weather_data in weather_data_json:
                
                # Informações da API interna | DataService API
                description = weather_data.get('descricao_weather')
                current_temp = weather_data.get('temperatura_atual')
                max_temp = weather_data.get('temperatura_max')
                min_temp = weather_data.get('temperatura_min')
                humidity = weather_data.get('umidade')
                wind_speed = weather_data.get('velocidade_vento')
                wind_direction = weather_data.get('direcao_vento')
                gust_wind = weather_data.get('rajada_vento')
                timestamp = weather_data.get('data_hora')

                # Análise #01: Calcular a média da temperatura do dia.
                if max_temp is not None and min_temp is not None:
                    
                    average_temp = (max_temp + min_temp) / 2
                else:
                
                    average_temp = "N/A"

                # Formatação final do Boletim
                weather_report = (
                    f"Newsletter - UFMS Dados Climáticos\n"
                    f"Timestamp: {timestamp}\n"
                    f"- Description: {description}\n"
                    f"- Current Temperature: {current_temp} °C\n"
                    f"- Max Temperature: {max_temp} °C\n"
                    f"- Min Temperature: {min_temp} °C\n"
                    f"- Average Temperature: {average_temp} m/s\n"
                    f"- Humidity: {humidity}%\n"
                    f"- Wind Speed: {wind_speed} m/s\n"
                    f"- Wind Direction: {wind_direction}°\n"
                    f"- Gust Wind: {gust_wind} m/s\n"
                    "-----------------------------\n"
                )

                weather_reports.append(weather_report)

            # print(weather_reports)
            return weather_reports
        
        except Exception as e:
            print(f"Failed to format weather data: {str(e)}")
            return None
    
    # 3. Enviar o email com o boletim
    def send_email_with_weather_data(self, to_email, weather_reports):
        """
            Executa a partir do email do usuario e a lista de relatórios criados e busca alinhar ao correspondente período de inscrição(frequency). 
            
                -> Então, é esperado que sejam enviados, para cada usuário do período `minute`, um relatório das condições climáticas atuais que foram setadas a partir do período de registro ao bd, por exemplo.
                      
        """
        try:
            if not self.mail:
                raise Exception("Mail object is not initialized. Call initialize_mail() first.")
            
            msg = Message("UFMS Weather Report", recipients=[to_email])
            msg.body = "\n".join(weather_reports)
            self.mail.send(msg) 
            return True
        
        except Exception as e:
            
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False

    # EmailLog
    def log_email(self, user_id, email, status):
        try:
            log = EmailLog(user_id=user_id, email=email, status=status)
            self.db.add(log)
            self.db.commit()
            print(f"Logging email status for {email}: {status}")
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao logar email: {str(e)}")
        finally:
            # Fecha a sessão
            self.db.close()
            
    # 4. Enviar a notificação aos usuários por frequência | JobSchedule
    def send_notifications(self):
        """
            Para cada usuário, verificar a frequência cadastrada e agendar o envio de emails com base na frequência.

        """
        try:
            users = self.db.query(User).all()
            for user in users:
                frequency = user.frequency
                if frequency == 'minute':
                    self.send_email_immediately(user.email)
                else:
                    self.schedule_email(user, frequency)
        except Exception as e:
            print(f"Failed to send notifications: {str(e)}")

    # Teste
    def send_email_immediately(self, to_email):
        try:
            weather_data = self.get_weather_data_from_api()
            if weather_data:
                weather_reports = self.formatar_boletim(weather_data)
                success = self.send_email_with_weather_data(to_email, weather_reports)
                if success:
                    print(f"Email sent successfully to {to_email}")
                    self.log_email(to_email, "Success")
                else:
                    print(f"Failed to send email to {to_email}")
                    self.log_email(to_email, "Failure")
            else:
                print(f"Failed to fetch weather data for {to_email}")
                self.log_email(to_email, "Failed to fetch weather data")
        except Exception as e:
            print(f"Failed to send email immediately to {to_email}: {str(e)}")

    # 6. Agendar os emails
    def schedule_email(self, user, frequency):
        """
            Agendar o envio de emails.
        """
        try:
            # Definir o trigger com base na frequência
            if frequency == 'daily':
                trigger = IntervalTrigger(days=1)
            elif frequency == 'weekly':
                trigger = IntervalTrigger(weeks=1)
            elif frequency == 'biweekly':
                trigger = IntervalTrigger(weeks=2)
            elif frequency == 'monthly':
                trigger = IntervalTrigger(weeks=4)
            elif frequency == 'semiannual':
                trigger = IntervalTrigger(months=6)
            else:
                print(f"Invalid frequency for user {user.email}")
                return
            
            # Adicionar job ao scheduler
            scheduler.add_job(
                func=self.send_email_with_weather_data,
                trigger=trigger,
                args=[user.email],
                id=f'send_email_{user.id}',
                replace_existing=True
            )
        except Exception as e:
            print(f"Failed to schedule email for {user.email}: {str(e)}")

