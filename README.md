  
![YaTube CI/CD](https://github.com/BystrovN/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Welcome!

Проект **YaMDb** собирает отзывы пользователей на различные произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят оценку в диапазоне от одного до десяти. Из оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.


## Документация

Подробный перечень запросов, параметров, необходимых прав доступа и примеров ответов находится в документации и расположен по адресу - **localhost/redoc/**
 

## Установка
Все команды терминала в данном разделе выполняются с правами суперпользователя. 

1. Для запуска проекта необходимо заполнить файл **.env** с переменными окружения. Важно, чтобы указанный файл находился в одной директории с **docker-compose.yaml**. Пример заполнения:
> DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
> DB_NAME=postgres # имя базы данных
> POSTGRES_USER=postgres # логин для подключения к базе данных
> POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
> DB_HOST=db # название сервиса (контейнера)
> DB_PORT=5432 # порт для подключения к БД
3. Для развертывания приложения необходимо из директории *infra/* выполнить команду:
```
	docker-compose up -d
```
	Флаг -d выполнит развертывание в фоновом режиме, что позволит осуществлять управление контейнерами из этого же окна терминала.
4. После запуска контейнера выполним миграции:
```
	docker-compose exec web python manage.py migrate
```
5. Создадим суперпользователя:
```
	docker-compose exec web python manage.py createsuperuser
```
	В проекте yamdb суперпользователь имеет право на создание, редактирование, удаление любых объектов по описанным в документации эндпоинтам. 
6. Для отображения внутренней статики выполним команду:
```
	docker-compose exec web python manage.py collectstatic --no-input
```
	Флаг --no-input позволит django перезаписывать обновленные файлы статики в директории STATIC_ROOT без вашего разрешения. 
7. Для ознакомления с возможностями сервиса в корневой директории  присутствует дамп заполненной базы данных - файл **fixtures.json**.  Для выгрузки применяется команда:
```
	docker-compose exec web python manage.py loaddata fixtures.json
```


## Технологии

 - Python - 3.8.15
 - Django - 2.2.16
 - Django Rest Framework - 3.12.4
 - Postgres - 13.0
 - Gunicorn - 20.0.4
 - Nginx - 1.21.3
 - Docker - 20.10.21
 - Docker Compose - 2.13.0
