from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser
from api.serializers import ComicSerializer
from api.models.ec.comic import Comic
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class ComicViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsEmployeeUser, IsAuthenticated)

    def list(self, request):
        employee = Employee.objects.get(user=self.request.user)
        comics = Comic.objects.filter(product__organization=employee.organization)
        serializer = ComicSerializer(comics, many=True)
        return Response(serializer.data)
