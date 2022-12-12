# Simple aplicación construida en Django

Basada en [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python).

Esta aplicación tiene un sistema de logueo básico, se pueden crear nuevos usuarios que utilicen la aplicación.
Está lista para ser deployada en Heroku.
Procesa archivos csv con determinado formato y permite bajarlos luego de ser procesados.

Para correr la aplicación en docker:

1. docker-compose up -d --build
2. Entrar al container de django y escribir:
   2.1) python manage.py migration
   2.2) python manage.py createsuperuser
