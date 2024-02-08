from rest_framework import serializers
from accounts.models import User
from django_countries.serializers import CountryFieldMixin
   

class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
        
    class Meta:
        model = User
        
        fields = [
            'id', 
            'date_joined', 
            'last_login', 
            'password', 
            'first_name', 
            'last_name',             
            'email', 
            'profile_pic', 
            'google_picture', 
           
        ]
        
