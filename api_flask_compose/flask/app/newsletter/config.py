import os
# ---------------- Confgurações NewsletterService ----------------
"""
    Ao subir o container via compose, as variáveis do postgres serão reconhecidas pelo arquivo `.env`
"""
# Flask + PostgreSQL 
DEBUG = True
DATABASE_URI = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB_NWS')}"

# Configurações do Flask-Mail
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') 
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


