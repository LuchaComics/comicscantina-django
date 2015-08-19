from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.pulllist import Pulllist
from api.serializers import PulllistSerializer


class PulllistViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Pulllist.objects.all()
    serializer_class = PulllistSerializer
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    filter_fields = ('series__series_id','organization__org_id', 'store__store_id', )
    search_fields = ('series__series_sort_name',)
