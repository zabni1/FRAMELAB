from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_after_registration(email) -> None:
    html = render_to_string('')
    msg = EmailMultiAlternatives(subject='Код для авторизації', to=[email])
    msg.attach_alternative(html, 'text/html')
    msg.send()

def send_email_after_login(email) -> None:
    html = render_to_string('')
    msg = EmailMultiAlternatives(subject='Код для авторизації', to=[email])
    msg.attach_alternative(html, 'text/html')
    msg.send()