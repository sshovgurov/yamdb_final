БЕЙДЖ - https://github.com/sshovgurov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg

Проект Yambd собирает отзывы о фильмах
Проект развернут на удаленном сервере, с помощью утилиты Ubuntu(WSL2)

1) Выполните вход на свой удаленный сервер с помощью wsl
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:
```bash
ssh <lusername>@<host>
```

2) Установите docker и docker-compose на сервер:
Введите команду:
```bash
sudo apt install docker.io
sudo apt  install docker-compose
```

3)Скопируйте подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер
Введите команду из корневой папки проекта:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r nginx/ <username>@<host>:/home/<username>/
```

4)Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных
```bash
SECRET_KEY=<SECRET_KEY>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль DockerHub>
USER=<логин для подключения к серверу>
HOST=<публичный IP сервера>
PASSPHRASE=<пароль для входа>
SSH_KEY=<публичный SSH ключ>
TELEGRAM_TO=<ID телеграм аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

5)Миграции, суперпользователь, загрузка статики (wsl)
```bash
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py createsuperuser
```

6) Технологии
wsl2 (Ubuntu), GitBash, Visual Studio Code, TabNine, Docker

7)Ссылка на DockerHub:
https://hub.docker.com/repository/docker/sshovgurov/infra_sp2_web

8)Ссылка на сервер:
http://51.250.3.62/admin/