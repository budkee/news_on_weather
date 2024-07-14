import os
# ---------------- Confgurações DataService ----------------
"""
    Variáveis do postgres serão reconhecidas pelo arquivo `api_flask_compose/.env`. 
"""

# Flask + PostgreSQL 
DEBUG = True
DATABASE_URI = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB_DATA')}"
