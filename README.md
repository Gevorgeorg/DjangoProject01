# MarketBoard - Доска объявлений

Платформа для размещения объявлений с Django бэкендом и React фронтендом.
Предназначен для создания сайтов с объявлениями.

## Что реализовано в этом проекте

**API работает с моделями и базой данных postgresql:**
- Реализованы модели пользователей, объявлений, комментариев и взаимосвязи между ними
- Осуществляется создание объявлений и комментариев
- Пагинация и поиск по названию объявлений
- Загрузка изображений для объявлений
- Реализована регистрация пользователей

**API использует JWT токены для аутентификации:**
- Регистрация: POST /api/users/
- Логин: POST /auth/token/login (выдача токенов)
- Обновление: POST /auth/token/refresh для получения новых токенов
- Есть ограничения прав для разных категорий пользователей

## Как запустить

```bash
# Клонируйте репозиторий
git clone https://github.com/Gevorgeorg/DjangoProject01.git
```
```bash
# Установите зависимости
pip install -r requirements.txt
```

```bash
# Создание виртуального окружение
python -m venv venv

# Активация окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```


### Заполните .env файл 

### Создайте и запустите PostgreSQL контейнер

```bash

docker run --name <имя контейнера> -e POSTGRES_DB=<имя БД> -e POSTGRES_USER=<имя пользователя> -e POSTGRES_PASSWORD=<пароль> -p 5432:5432 -d postgres:13
```
### Выполните миграции

```bash

python manage.py makemigrations
python manage.py migrate
```

# Запуск приложения:

```bash

# Backend
python manage.py runserver
```

```bash

# Frontend

# Перейти в папку с фронтендом
cd frontend_react

# Установка зависимостей
npm install

# Запуск разработки
npm start


#Фронтенд будет доступен по адресу: http://localhost:3000
```
