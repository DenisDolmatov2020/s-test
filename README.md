S-Test

git clone https://github.com/DenisDolmatov2020/s-test.git

cd sTest

в файле docker-compose.yml основные настройки сайта и отправки почты

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

docker-compose build

docker-compose up