# ironbell
Kettlebell competition scoring website

To be added: Docker info for dev environment

The competition site can be started via the Docker container interactive prompt.
Run the following commands in /usr/local/ironbell/scoring/

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Subsequently, only the last command needs to be run to restart the server.

Visit the following urls in a browser on the host:

http://localhost:8000
http://localhost:8000/admin

