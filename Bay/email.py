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

def send_user_order_receipt(name,receiver,orders,acc_ref,total):
    send_order=sendgrid.helpers.mail.Mail(
        from_email='pyramyra33@gmail.com',
        to_emails=receiver,
        subject="Order received for processing",
        html_content=render_to_string('order.html',{"name":name,"orders":orders,"receipt_no":acc_ref,"total":total})
    )
    sg=SendGridAPIClient(SENDGRID_API_KEY)
    res=sg.send(send_order)

def user_made_order(name,sender,phone,orders,acc_ref,total):
    send_us_order=sendgrid.helpers.mail.Mail(
        from_email=sender,
        to_emails='pyramyra33@gmail.com',
        subject='Customer Order: '+name,
        html_content=render_to_string('send_purchase.html',{"name":name,"orders":orders,"receipt_no":acc_ref,"total":total,"phone":phone})
    )
    sg=SendGridAPIClient(SENDGRID_API_KEY)
    res=sg.send(send_us_order)
