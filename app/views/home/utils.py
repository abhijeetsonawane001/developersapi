from app import mail
from flask_mail import Message
from flask import render_template


def send_login_mail(receiver, login_otp):
    body_message = render_template(
        "emails/login_otp/login_otp.txt", login_otp=login_otp
    )
    html_message = render_template(
        "emails/login_otp/login_otp.html", login_otp=login_otp
    )

    msg = Message(subject="DevelopersAPI Login", recipients=[receiver])
    msg.body = body_message
    msg.html = html_message

    mail.send(msg)
