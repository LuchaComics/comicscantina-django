from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt


@login_required(login_url='/mobile/pos/login')
def dashboard_page(request, store_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})
        
    employee = Employee.objects.get(user__id=request.user.id)
        
    try:
        receipts = Receipt.objects.filter(
            has_purchased_online=False,
            has_finished=False,
            employee=employee,
        )
    except Receipt.DoesNotExist:
        receipts = None
        
    return render(request, 'mobile_pos/dashboard.html',{
        'store': store,
        'employee': employee,
        'receipts': receipts,
        'page': 'dashboard',
    })
