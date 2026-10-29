# Learning Log

Основной проект курса Django: пользователь создаёт собственные темы обучения, добавляет к ним записи и видит только свои данные.

## Возможности

- регистрация, вход и безопасный POST-выход;
- личные темы и записи, создание и редактирование;
- защита от просмотра или изменения чужих тем и записей;
- административный интерфейс для преподавателя/администратора;
- адаптивный интерфейс Bootstrap 4.

## Локальный запуск

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Для админ-панели создайте администратора: `.venv/bin/python manage.py createsuperuser`.

## Проверка

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

## Docker и учебный сервер

1. Скопируйте пример: `cp .env.example .env`.
2. Задайте уникальный `DJANGO_SECRET_KEY`, разрешённые хосты и порт.
3. Локально выполните `docker compose up -d --build`.

На учебном сервере укажите выданный проекту `APP_PORT`, внешний `APP_BIND_IP=0.0.0.0`, IP с портом в `DJANGO_CSRF_TRUSTED_ORIGINS` и затем выполните ту же команду. Docker-том `learning_log_data` сохраняет SQLite-базу между пересборками; не используйте `docker compose down -v`, если данные нужны.

Не публикуйте `.env`, базу данных и виртуальные окружения.
