from django.core.mail import send_mail
import random
from django.conf import settings
from accounts.models import User

def sendMail(email):
   
    subject = 'Your account verification email'
    otp = random.randint(1000, 9999)
    # message = "test message"
    message = ("Your otp is {}").format(otp)
    email_from = settings.EMAIL_HOST 
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
