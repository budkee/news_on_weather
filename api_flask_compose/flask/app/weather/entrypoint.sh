#!/bin/sh

echo "| --------------- Iniciando Weather App ------------------ |"
# gunicorn --bind 0.0.0.0:5002 wsgi:app 
gunicorn -w 2 --bind 0.0.0.0:5002 wsgi:app &
# Manter o contêiner rodando
tail -f /dev/null
