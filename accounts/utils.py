from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from accounts.functions.reset_password_mail import HTML_FORMAT, LINK_BUTTON
from accounts.functions.reset_password_email import HTML_FORMAT, LINK_BUTTON, OTP_NUMBER, OTHER
import random
from accounts.models import User

import smtplib

class Util:

  def send_email(data):
    subject = 'Réinitialisez votre mot de passe'
    otp = random.randint(1000, 9999)
    html_content = HTML_FORMAT + LINK_BUTTON.format(link=data['body']) + OTP_NUMBER.format(otp=otp) + OTHER
    body = MIMEText(html_content, _subtype='html')
    from_email = settings.EMAIL_HOST_USER
    # to = [data['to_email']]
    email = MIMEMultipart(_subtype='related')
    email['From'] = from_email
    email['Subject'] = subject
    email['To'] = data['to_email']
    email.attach(body)
    # text = email.as_bytes()
    # subject = data['subject']
    # body = data['body']
    
    # send_mail( from_email, email['To'].split(","), text)
    try:
        server = smtplib.SMTP_SSL(settings.EMAIL_HOST)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        text = email.as_bytes()
        server.sendmail(from_email, email['To'], text)
        
        user_obj = User.objects.get(email=email['To'])
        user_obj.otp = otp

        user_obj.save()
        
        server.quit()
        
        return True
    except Exception as e:
        print('Failed to send email:', e)
        return False
    
#   def send_confirmation_email(data):
#     subject = 'Confirmation inscription '
#     html_content = HTML_FORMAT2
#     body = MIMEText(html_content, _subtype='html')
#     from_email = settings.EMAIL_HOST_USER

#     email = MIMEMultipart(_subtype='related')
#     email['From'] = from_email
#     email['Subject'] = subject
#     email['To'] = data['to_email']
#     email.attach(body)

#     try:
#         server = smtplib.SMTP_SSL(settings.EMAIL_HOST)
#         server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         text = email.as_bytes()
#         server.sendmail(from_email, email['To'], text)
#         server.quit()
#         return True
#     except Exception as e:
#         print('Failed to send email:', e)
#         return False