from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.serializers import PulllistSubscriptionSerializer


class PulllistSubscriptionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = PulllistSubscription.objects.all()
    serializer_class = PulllistSubscriptionSerializer
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('customer__customer_id', 'pulllist__pulllist_id', 'organization__org_id',)

