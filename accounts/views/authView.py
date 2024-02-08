from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from accounts.functions.emails import *

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions

from accounts.functions.checkPassword import password_check

import random
from accounts.serializers.inputSerializers import (ChangePasswordSerializer,
                                                   LoginSerializer,
                                                   ResetPasswordEmailRequestSerializer,
                                                   SendPasswordResetEmailSerializer,
                                                   SetNewPasswordSerializer,
                                                   GoogleOauthSerializer
                                                   )
from accounts.serializers.outputSerializers import UserSerializer

from accounts.functions.checkToken import token_expire_handler, expires_in
from accounts.authentication import ExpiringTokenAuthentication
from accounts.models import User
from accounts.functions.login_user import login_user

# from accounts.pagination import BasicPagination, PaginationHandlerMixin


@authentication_classes([ExpiringTokenAuthentication])
class AuthViews(ViewSet):
    serializer_class = UserSerializer
    google_oauth_serializer = GoogleOauthSerializer

    def list(self, request):
        return Response({"detail": "this is the auth base url"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='register', url_name='register')
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not password_check(request.data["password"]):
                return Response({"detail": "your password is too weak"}, status=status.HTTP_400_BAD_REQUEST)

            password = make_password(request.data["password"])
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='login', url_name='login')
    def login(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            try:
                account = User.objects.get(email=email)
            except:

                account = get_object_or_404(User, email=email)

            if not check_password(password, account.password):
                data = {"detail": "incorrect login credentials"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            if account.is_active:
                token, _ = Token.objects.get_or_create(user = account)
                token = token_expire_handler(token)
                serializer = self.serializer_class(account, many=False)
                data = serializer.data
                data['expired_in'] = expires_in(token)
                data['token'] = token.key
                update_last_login(None, account)
                return Response(data, status=status.HTTP_200_OK) 

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='change-password', url_name='change-password', permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not check_password(serializer.data['oldPassword'], request.user.password):
                return Response({"detail": "wrong old password"}, status=status.HTTP_400_BAD_REQUEST)

            if not password_check(serializer.data['newPassword']):
                return Response({"detail": "password is too weak"}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, pk=request.user.pk)
            user.set_password(serializer.data["newPassword"])
            token, _ = Token.objects.get_or_create(user=request.user)
            token.delete()
            user.save()
            return Response({"detail": "password updated successfuly"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='reset-password-email', url_name='reset-password-email', permission_classes=[AllowAny])
    def reset_password_email(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        # serializer = ResetPasswordEmailRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['post'], name='reset-password', url_name='reset-password', permission_classes=[AllowAny])
    def reset_password(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = User.objects.filter(email=email)
            if not user.exists():
                return Response({"details": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({"details": "Wrong otp"}, status=status.HTTP_400_BAD_REQUEST)

            if not password_check(request.data["password"]):
                return Response({"detail": "your password is too weak"}, status=status.HTTP_400_BAD_REQUEST)

            if request.data["password"] != request.data['confirmPassword']:
                return Response({"detail": "Password do not match "}, status=status.HTTP_400_BAD_REQUEST)

            user = user.first()
            user.password = make_password(request.data["password"])
            user.save()
            return Response({"detail": "password reset successfuly"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='logout', url_name='logout', permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        data = {"detail": "successfully log out "}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='verify', url_name='verify', permission_classes=[IsAuthenticated])
    def verify(self, request):
        data = {"detail": "successfully log in "}
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], name='google', url_name='google', permission_classes=[AllowAny])
    def google(self, request):
        serializer = self.google_oauth_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            google_picture = serializer.data["google_picture"]
            
            account, _ = User.objects.get_or_create(email=email)
            
            if _ or (not _ and account.google_login):
                account.first_name = first_name
                account.last_name = last_name
                account.google_picture = google_picture
                account.is_active = True
                account.google_login = True
                account.save()
                
                if account.is_active:
                    data = login_user(account)
                    return Response({
                        "status": True,
                        "message": "You are successfully logged in",
                        "detail": data
                    }, status=status.HTTP_200_OK)
                return Response({
                    "status": True,
                    "message": "Your account is inactive, please contact the administrator",
                }, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "status": False,
                "message": "This email is already connected with a password",
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": False,
            "message": "Invalid data entered",
            "detail": serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)
