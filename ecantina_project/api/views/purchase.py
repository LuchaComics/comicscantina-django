from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser
from api.serializers import PurchaseSerializer
from api.models.ec.purchase import Purchase
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class PurchaseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsEmployeeUser, IsAuthenticated)

    def list(self, request):
        employee = Employee.objects.get(user=self.request.user)
        purchases = Purchase.objects.filter(product__organization=employee.organization)
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)
