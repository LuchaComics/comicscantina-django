from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'carts': reverse('carts-list', request=request, format=format),
        'comics': reverse('comics-list', request=request, format=format),
        'customers': reverse('customers-list', request=request, format=format),
        'employees': reverse('employees-list', request=request, format=format),
        'products': reverse('products-list', request=request, format=format),
    })