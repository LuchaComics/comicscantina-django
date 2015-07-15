import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from inventory.models.ec.organization import Organization
from inventory.models.ec.employee import Employee
from inventory.models.ec.store import Store
from inventory.models.ec.comic import Comic


@login_required(login_url='/inventory/login')
def print_label_comics_page(request, org_id, store_id):
    # Fetch all the comics starting with the most recent submission
    # grouped by the most recent submission date.
    q = Comic.objects.filter(store_id=store_id)
    q = q.order_by('created')
    q.query.group_by = ['created']
    
    paginator = Paginator(q, 100) # Show 100 comics per page
    page = request.GET.get('page')
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comics = paginator.page(paginator.num_pages)
    
    return render(request, 'inventory/print_label/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'comics': comics,
        'tab':'print',
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
