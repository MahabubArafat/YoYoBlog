from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

#current_app nijei ekta instance of our app, mane flask ere create kore rakhe application ta pass kore, so ekta argument hisebe current app amra pass korte pari na, so ejonno current_app je object ta re currently represent kortese with help of flask,we can get it by _get_current_object()