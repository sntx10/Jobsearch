from config.celery import app
from django.core.mail import send_mail
from decouple import config

@app.task
def send_confirmation_email(email, code):
    full_link = f'http://127.0.0.1:8000/account/confirm/{code}'
    send_mail(
        'User activation',
        f'Пажалуйста подтвердите аккаунт перейдя по ссылке: {full_link}',
        config('EMAIL_HOST_USER'),
        [email]
    )
