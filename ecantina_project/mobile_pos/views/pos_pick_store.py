from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt


@login_required(login_url='/mobile/pos/login')
def pick_store_page(request):
    try:
        employee = Employee.objects.get(user__id=request.user.id)
        stores = Store.objects.filter(organization=employee.organization)
    except Store.DoesNotExist:
        stores = None

    return render(request, 'mobile_pos/pick_store.html',{
        'stores': stores,
        'page':'pick_store',
    })