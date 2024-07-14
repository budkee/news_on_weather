FROM nginx:alpine

COPY /conf.d/nginx.conf /etc/nginx/nginx.conf

# COPY flask/app/static /usr/share/nginx/html

# Remove o erro de 502 Bad Gateway
RUN chmod 775 /

# Comando para iniciar o Nginx
CMD [ "nginx", "-g", "daemon off;" ]

