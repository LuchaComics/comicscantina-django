from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import CategorySerializer
from api.models.ec.tag import Tag
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.promotion import Promotion
from api.models.ec.category import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly, IsAuthenticatedOrReadOnly,)
