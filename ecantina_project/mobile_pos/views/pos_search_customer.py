from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt


@login_required(login_url='/mobile/pos/login')
def search_customer_page(request, store_id=0, receipt_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})
    
    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None

    return render(request, 'mobile_pos/search_customers.html',{
        'receipt': receipt,
        'store': store,
        'employee': employee,
        'page': 'cart',
    })