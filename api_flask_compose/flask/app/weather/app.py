import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from flask import Flask, request, jsonify, make_response, send_from_directory, render_template
from flask_restx import Api, Resource, fields
from weather_service import OpenWeatherMapClient, parse_weather_data
from weather_repository import WeatherRepository

# ---------------- Data App + Swagger Doc ----------------
app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app, version='1.4', title='Serviço de Coleta de Dados',
          description='Serviço de coleta de dados meteorológicos.')
ns = api.namespace('weather', description='Serviço de coleta de dados meteorológicos.')


# ---------------- Modelagem dos dados ----------------

location_model = api.model('Location', {
    'latitude': fields.Float(required=True, description='The latitude'),
    'longitude': fields.Float(required=True, description='The longitude'),
    'nome': fields.String(description='The name of the location')
})

weather_data_model = api.model('WeatherData', {

    'data_hora': fields.DateTime(description='Timestamp of the data'),
    'localizacao': fields.Nested(api.model('Localizacao', {
        
        'latitude': fields.Float(description='The latitude'),
        'longitude': fields.Float(description='The longitude'),
        'nome': fields.String(description='The name of the location')
    
    })),
    'descricao_weather': fields.String(description='Weather description'),
    'temperatura_atual': fields.Float(description='Current temperature'),
    'temperatura_max': fields.Float(description='Maximum temperature'),
    'temperatura_min': fields.Float(description='Minimum temperature'),
    'umidade': fields.Float(description='Humidity'),
    'velocidade_vento': fields.Float(description='Wind speed'),
    'direcao_vento': fields.Float(description='Wind direction'),
    'rajada_vento': fields.Float(description='Wind gust speed')
})

pagination_model = api.model('Pagination', {
    
    'limit': fields.Integer(description='Limit of records per page'),
    'page': fields.Integer(description='Page number')
    
})
"""
    Serviço de coleta de dados periódicos

    - Coleta de dados agendada para ser feita uma vez por dia.
"""
def collect_weather_data():
    with app.app_context():
        
        latitude = 37.09024
        longitude = -95.712891
        nome = 'UFMS'

        owm_client = OpenWeatherMapClient(os.getenv('API_KEY'))
        weather_data = owm_client.get_weather_data(latitude, longitude)
        parsed_data = parse_weather_data(weather_data)

        repo = WeatherRepository()
        localizacao = {"latitude": latitude, "longitude": longitude, "nome": nome}
        saved_localizacao = repo.save_localizacao(localizacao)
        repo.save_condicoes_climaticas(saved_localizacao.id, parsed_data)


scheduler = BackgroundScheduler()
# scheduler.add_job(collect_weather_data, trigger='interval', seconds=5) # Coleta rápida
scheduler.add_job(collect_weather_data, CronTrigger(hour=0, minute=1))
scheduler.start()

# ---------------- Rotas/Endpoints ----------------
@app.route('/home')
def index():
    return render_template('index.html')

"""
    Fixamos a lat e longitude da ufms, ta salvando no banco de dados certinho.

"""
# [POST] rota: /weather/collect | Respostas {'201': sucesso, '400': falha}
@ns.route('/collect', methods = ['POST'])
class CollectWeatherData(Resource):
    
    @ns.expect(location_model)
    @ns.response(201, 'Dados climáticos atuais coletados com sucesso!')
    @ns.response(400, 'Invalid input')
    def post(self):
        # ----------- Execução do Serviço ----------- 
        
        collect_weather_data()
        # Response enviada no email #01
        return {"message": "Dados climáticos atuais coletados com sucesso!"}, 201


# [GET] rota: /weather/data | Limite de 10 registros por página
@ns.route('/data', methods = ['GET'])
class ListWeatherData(Resource):
    
    @ns.expect(pagination_model)
    @ns.marshal_list_with(weather_data_model)
    def get(self):
        # Endpoint de acesso: http://127.0.0.1:5002/weather/data?limit=2&page=1
        # ---------------- Parâmetros de visualização ----------------
        try:
            limit = int(request.args.get('limit', 10))
            page = int(request.args.get('page', 1))
        
            # Ensure limit and page are positive integers
            if limit < 1:
                limit = 10
            if page < 1:
                page = 1

            # Cap the limit to 10
            limit = min(limit, 10)

            # ---------------- Paginação ----------------
            offset = (page - 1) * limit

            # ---------------- Instância do Repositório ----------------
            repo = WeatherRepository()
            data = repo.get_paginated_data(limit, offset)

            # ---------------- Formatação dos Registros ----------------
            result = [{
                'data_hora': record.data_hora,
                'localizacao': {
                    'latitude': record.localizacao.latitude,
                    'longitude': record.localizacao.longitude,
                    'nome': record.localizacao.nome
                },
                'descricao_weather': record.descricao_weather,
                'temperatura_atual': record.temperatura_atual,
                'temperatura_max': record.temperatura_max,
                'temperatura_min': record.temperatura_min,
                'umidade': record.umidade,
                'velocidade_vento': record.velocidade_vento,
                'direcao_vento': record.direcao_vento,
                'rajada_vento': record.rajada_vento
            } for record in data]

            # Handle X-Fields header
            fields_mask = request.headers.get('X-Fields')
            if fields_mask:
                fields_mask = fields_mask.split(',')
                result = [{k: v for k, v in record.items() if k in fields_mask} for record in result]

        except ValueError:
            return jsonify({"error": "Invalid limit or page parameter"}), 400

        # ---------------- Retorna os dados e o status ----------------
        return result, 200

# [GET] rota: /weather/latest_data | Lista os 10 últimos registros coletados
@ns.route('/latest_data', methods=['GET'])
class LatestWeatherData(Resource):
    @ns.marshal_list_with(weather_data_model)
    def get(self):
        repo = WeatherRepository()
        data = repo.get_latest_data(limit=10)
        result = [{
                'data_hora': record.data_hora,
                'localizacao': {
                    'latitude': record.localizacao.latitude,
                    'longitude': record.localizacao.longitude,
                    'nome': record.localizacao.nome
                },
                'descricao_weather': record.descricao_weather,
                'temperatura_atual': record.temperatura_atual,
                'temperatura_max': record.temperatura_max,
                'temperatura_min': record.temperatura_min,
                'umidade': record.umidade,
                'velocidade_vento': record.velocidade_vento,
                'direcao_vento': record.direcao_vento,
                'rajada_vento': record.rajada_vento
            } for record in data]
        
        return result, 200


# ---------------- Início da Aplicação ----------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

