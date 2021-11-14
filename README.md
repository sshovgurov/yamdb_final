БЛОК 1 - WORKFLOW
1)Создайте workflow для репозитория yamdb_final на GitHub Actions. Опишите workflow в файле .github/workflows/yamdb_workflow.yml DONE
В workflow должны быть четыре job:
2)Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final. DONE
3)Сборка и доставка докер-образов на Docker Hub.
4)Автоматический деплой проекта на боевой сервер.
5)Отправка уведомления в Telegram.
6)Добавьте в файл README.md бейдж, показывающий статус вашего workflow.

БЛОК 2 - Для успешной работы сервер необходимо подготовить.
1)Остановите службу nginx;
2)Установите docker. Для этого выполните команду:
sudo apt install docker.io 
3)Установите docker-compose, в этом вам поможет официальная документация.
Скопируйте подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.
Копирование этих файлов выполняется вручную: их настройка, как правило, выполняется один раз и изменения в эти файлы вносятся крайне редко.
3)Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных ; отредактируйте инструкции workflow для задачи deploy


Чек-лист для самопроверки
1)В файл docker-compose.yaml описаны инструкции для трёх контейнеров: web, db, nginx.
2)Настроены volumes для базы данных, статики и медиа (файлов, загружаемых пользователями).
3)Директория .github/workflows содержит корректный workflow в файле yamdb_workflow.yaml.
4)Проект развёрнут и запущен на боевом сервере.
5)При пуше в ветку main код автоматически деплоится на сервер.
6)В репозитории в файле README.md установлен бейдж о статусе работы workflow.


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