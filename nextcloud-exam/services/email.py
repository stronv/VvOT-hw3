from flask_mail import Message

from app import mail


def send_message(subject, body, recipient):
    message = Message(
        subject=subject,
        recipients=[recipient],
    )
    message.body = body
    mail.send(message)
