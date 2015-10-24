from django.conf import settings
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCompanyPolicy
from api.serializers import EmployeeSerializer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class EmployeeViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCompanyPolicy, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username', '=user__email')