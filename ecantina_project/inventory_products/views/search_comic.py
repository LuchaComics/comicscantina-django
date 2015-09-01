import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.story import GCDStory
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from inventory_products.forms import IssueForm


@login_required(login_url='/inventory/login')
def search_comics_page(request, org_id, store_id):
    return render(request, 'inventory_products/comic/search_gcd/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'add',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required(login_url='/inventory/login')
def search_products_page(request, org_id, store_id):
    return render(request, 'inventory_products/comic/search_ec/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'prduct_comics',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })