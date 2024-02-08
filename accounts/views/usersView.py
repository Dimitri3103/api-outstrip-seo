from django.shortcuts import get_object_or_404


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions



from accounts.serializers.outputSerializers import UserSerializer
from accounts.authentication import ExpiringTokenAuthentication
from accounts.models import User
from accounts.pagination import BasicPagination, PaginationHandlerMixin


# UserView   
class UserViews(ViewSet,PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        user = User.objects.all().exclude(email=request.user.email).exclude(is_staff=True).exclude(is_active=False)
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = User.objects.get(pk=pk)
        if request.data["password"] == "":
            instance.bio = request.data["bio"]
            instance.save()
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = User.objects.filter(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    