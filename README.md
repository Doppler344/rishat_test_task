# Rishat Test Task


## Features
- Запуск используя Docker
- Использование environment variables
- Просмотр Django Моделей в Django Admin панели
- Запуск приложения на удаленном сервере, доступном для тестирования
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
- Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме
- Добавлено поле Item.currency на две разные валюты и в зависимости от валюты выбранного товара предлагается оплата в соответствующей валюте


## Installation

Requires [Python](https://www.python.org//) v3.10+ to run.

Use virtual enviroment.

```
python3 -m venv
```

Clone repo 

```
git clone https://github.com/Doppler344/rishat_test_task
```
Install requirements

```
pip install -r requirements.txt
```
Next step you need create .env file for secret keys. Check here - https://django-environ.readthedocs.io/en/latest/quickstart.html 
> Check settings.py, create django secret key for .env - https://djecrety.ir/
> 
> Register at https://stripe.com/ for get stripe keys

Add all Secret keys to .env



Migrate to DB with django ORM

```
django makemigrations
django migrate
```

Create superuser for django admin with login and password
```
python manage.py createsuperuser
```
Run django server
```
python manage.py runserver
```

Congratulations!

**Grigoryan Dmitry**
