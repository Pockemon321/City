# Сделаем лучше вместе!

Веб-портал для управления городскими проблемами и их решением. Платформа позволяет жителям города сообщать о различных проблемах в городской инфраструктуре и следить за процессом их решения.

## Функциональность

- Регистрация и авторизация пользователей
- Создание заявок о проблемах с фотографиями "до" и "после"
- Категоризация проблем (дороги, освещение, благоустройство и т.д.)
- Отслеживание статуса заявок
- Административная панель для управления заявками
- Панель управления категориями
- Адаптивный дизайн для мобильных устройств

## Технологии

- Python 3.11+
- Django 5.0.2
- Bootstrap 4.5.2
- SQLite
- Crispy Forms
- Pillow для обработки изображений

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/city-problems-portal.git
cd city-problems-portal
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Добавьте начальные категории:
```bash
python manage.py add_initial_categories
```

7. Соберите статические файлы:
```bash
python manage.py collectstatic
```

8. Запустите сервер:
```bash
python manage.py runserver
```

9. Откройте в браузере: http://127.0.0.1:8000

## Структура проекта

- `main/` - основное приложение
  - `models.py` - модели данных (Request, Category)
  - `views.py` - представления
  - `forms.py` - формы
  - `admin.py` - настройки админ-панели
- `templates/` - шаблоны
- `static/` - статические файлы (CSS, JavaScript, изображения)
- `media/` - загруженные пользователями файлы

## Категории проблем

- Дороги и тротуары
- Освещение
- Детские площадки
- Озеленение
- Уборка территории
- Коммунальные услуги
- Общественный транспорт
- Парковки
- Вывоз мусора
- Благоустройство дворов

## Лицензия

MIT
