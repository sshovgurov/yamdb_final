БЕЙДЖ - https://github.com/sshovgurov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg

Проект Yambd собирает отзывы о фильмах
Проект развернут на удаленном сервере, с помощью утилиты Ubuntu(WSL2)

1)Если у вас Windows 10, и вы не установили WSL — у вас могут возникнуть проблемы с работой виртуализации системы и при запуске Docker. Установите подсистему Linux по [ссылке](https://docs.microsoft.com/ru-ru/windows/wsl/install) , затем выполняйте установку Docker.
Зайдите на [официальный сайт](https://www.docker.com/products/docker-desktop) проекта и скачайте установочный файл Docker Desktop для вашей операционной системы. [Docker Compose](https://docs.docker.com/compose) будет установлен автоматически. В Linux убедитесь, что у вас установлена последняя версия [Compose](https://docs.docker.com/compose/install/). Также вы можете воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

2)Клонируйте репозиторий и установите окружение(GitBash)
```bash
git clone https://github.com/sshovgurov/infra_sp2.git
python -m venv venv
pip install -r requirements.txt
```

3)В корневой папке репозитория создайте файл .env и поместите туда следующий код:
```bash
SECRET_KEY='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

4)docker-compose (wsl)
Для развёртывания приложения на основе контейнеров Docker нужно перейти в корневую директорию проекта и оттуда выполнить следующую команду: 
```bash
docker-compose up -d
```
Остановить работу всех контейнеров можно командой
```bash
docker-compose down
```

5)Миграции, суперпользователь, загрузка статики (wsl)
```bash
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
6)Тестирование проекта (bash)
```bash
pytest (убедитесь, что установили все необходимые зависимости)
```

7) Технологии
wsl2 (Ubuntu), GitBash, Visual Studio Code, TabNine, Docker

8)Ссылка на DockerHub:
https://hub.docker.com/repository/docker/sshovgurov/infra_sp2_web

9)Ссылка на сервер: