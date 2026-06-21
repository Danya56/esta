from django.core.mail import send_mail
from django.conf import settings

def send_client_email(client: dict):
    subject = f'Новая заявка от {client.get("name")}' 
    
    full_message = f"Сообщение создано автоматически! Тест заявки сайта: Имя клиента:{client.get('name')}\nНомер телефона: {client.get('phone')}\nАдрес почты: {client.get('email')}\n{client.get('message')}"

    send_mail(
        subject=subject,
        message=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['danil.goryunov.2020@gmail.com', 'npoesta@bk.ru'],
        fail_silently=False,
    )
