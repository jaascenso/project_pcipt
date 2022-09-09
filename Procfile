release: python manage.py makemigrations && python manage.py migrate
web: gunicorn projeto.wsgi --log-file=-