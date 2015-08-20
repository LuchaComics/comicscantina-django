from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsAdminUserOrReadOnly
from api.models.gcd.series import Series
from api.serializers import SeriesSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = (IsAdminUserOrReadOnly, IsAuthenticated)
    search_fields = ('name', )
    filter_fields = ('publisher',)

