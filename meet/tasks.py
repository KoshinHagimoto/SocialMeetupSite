from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import get_template

import SocialMeetup.settings as settings

@shared_task
def send_email(message):
    subject = 'データ更新'
    from_address = settings.DEFAULT_FROM_EMAIL
    to_address = [settings.DEFAULT_TO_EMAIL]
    send_mail(subject, message, from_address, to_address)

@shared_task()
def send_email_event(item, message):
    subject = 'イベント作成'
    from_address = settings.DEFAULT_FROM_EMAIL
    to_address = [settings.DEFAULT_TO_EMAIL]
    for member in item.group.member.all():
        to_address.append(member.email)
    send_mail(subject, message, from_address, to_address)

def get_message(item, action):
    if action == 'event':
        template = get_template('mail/message_event.txt')
    else:
        template = get_template('mail/message.txt')
    context = {
        "item": item, "action": action,
    }
    message = template.render(context)
    return message


def send_notification(item, action):
    message = get_message(item, action)
    if action == 'event':
        send_email_event(item, message)
    else:
        send_email.delay(message)