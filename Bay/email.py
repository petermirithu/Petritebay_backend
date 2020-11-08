import os
from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import sendgrid
from django.template.loader import render_to_string
# from django.core.mail import send_mail
from Petrite_Bay.settings import SENDGRID_API_KEY


def send_us_a_message(name,sender,subject,message):  
    user_sub=sendgrid.helpers.mail.Mail(
        from_email=sender,
        to_emails="pyramyra33@gmail.com",
        subject=subject,
        html_content=render_to_string('email.html',{"name":name,"message":message})
    )
    sg=SendGridAPIClient(SENDGRID_API_KEY)
    res=sg.send(user_sub)
