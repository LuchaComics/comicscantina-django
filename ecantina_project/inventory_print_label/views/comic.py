import json
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product
from api.models.ec.comic import Comic


@login_required(login_url='/inventory/login')
def comics_print_labels_page(request, org_id, store_id):
    # Fetch all the comics starting with the most recent submission
    # grouped by comic series.
    q = Comic.objects.filter(store_id=store_id)
    q = q.order_by('created')
    q.query.group_by = ['series']

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
    return render(request, 'inventory_print_label/comic/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'comics': comics,
        'tab':'print',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })
