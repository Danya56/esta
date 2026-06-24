from django.core.mail import send_mail
from django.conf import settings

def send_client_email(client: dict):
    subject = f'Новая заявка от {client.get("name")}' 
    
    full_message = (
    f"Заявка с сайта ESTA56\n"
    f"=======================\n\n"
    f"👤 Имя клиента: {client.get('name')}\n"
    f"📞 Телефон: {client.get('phone')}\n"
    f"✉️ Email: {client.get('email', 'Не указан')}\n\n"
    f"=======================\n"
    f"💬 Данные заявки / Комментарий:\n"
    f"{client.get('message', 'Комментарий отсутствует.')}"
)

    send_mail(
        subject=subject,
        message=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['danil.goryunov.2020@gmail.com'], #'npoesta@bk.ru'
        fail_silently=False,
    )
