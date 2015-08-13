from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsOnlyOwnedByOrganization
from api.serializers import SectionSerializer
from api.models.ec.section import Section


class SectionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsOnlyOwnedByOrganization, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('organization', 'store',)
