from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, GroupSerializer
from api.pagination import LargeResultsSetPagination
from api.permissions import IsEmployeeUser

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticated, IsEmployeeUser)


class GroupViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited.
        """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticated, IsEmployeeUser)