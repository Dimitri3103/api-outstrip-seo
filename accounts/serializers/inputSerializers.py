from rest_framework import serializers
from accounts.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from accounts.utils import Util



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=30)

class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=30)
    newPassword = serializers.CharField(max_length=30)
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    confirmPassword = serializers.CharField(min_length=8, max_length=68, write_only=True)
    otp = serializers.CharField()
  
    class Meta:
        fields = ['password', 'confirmPassword','otp']

class GoogleOauthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    google_picture = serializers.CharField(max_length=300)        


class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      link = 'http://localhost:3005/auth/confirm-password/'
      body = link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')    
    

 




