from flask_mail import Mail, Message
from models import *

class Config:
    """
       Класс настроек приложения Flask
    """
    # Включаем отладку приложения Flask
    DEBUG = True
    # Настройки расширения Flask-Mail
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # Используем переменные окружения для инициализации логина и пароля
    MAIL_USERNAME = 'timoshaborisov@yandex.ru'
    MAIL_PASSWORD = 'grunt1200'

app.config.from_object(Config)

mail = Mail(app)