from flask_mail import Mail, Message
import os

mail = Mail()

def send_email(subject, recipients,html_body):
    msg = Message(subject, sender=os.getenv('EMAIL_USER','user@email.com'), recipients=recipients)
    #msg.text = text_body
    msg.html = html_body
    mail.send(msg)