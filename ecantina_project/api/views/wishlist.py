from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.wishlist import Wishlist
from api.serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('customer', 'wishlist_id',)

