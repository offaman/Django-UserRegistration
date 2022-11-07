from userAccouts import settings
from django.core.mail import send_mail



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def send_mail_for_account_deletion(email,token):
    subject = 'We have received a request for account deletion'
    message = f'Hi paste the link to delete account http://127.0.0.1:8000/delete/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)

def send_mail_for_change_password(email,token):
    subject = 'We have received a request for passwordchange'
    message = f'Hi paste the link to change password http://127.0.0.1:8000/changepassword/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)