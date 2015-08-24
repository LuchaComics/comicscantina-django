import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue
from api.models.gcd.story import GCDStory
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from inventory.forms.issueform import IssueForm


@login_required(login_url='/inventory/login')
def list_comics_page(request, org_id, store_id):
    return render(request, 'inventory/list_inventory/comic/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'comic_list',
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def ajax_search_comics(request, org_id, store_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            series_text = request.POST['series']
            issue_num_text = request.POST['issue_num']
            publisher_text = request.POST['publisher']
            genre_text = request.POST['genre']
            from_text = request.POST['from']
            to_text = request.POST['to']
            comics = find_comics(
                org_id,
                store_id,
                series_text,
                issue_num_text,
                publisher_text,
                genre_text,
                from_text,
                to_text
            )
    return render(request, 'inventory/list_inventory/comic/list.html',{
        'comics' : comics,
    })


def find_comics(org_id, store_id, series_text, issue_num_text, publisher_text, genre_text, from_text, to_text):
    try:
        # Lookup 'Series'.
        q = Comic.objects.filter(issue__series__sort_name__icontains=series_text)
        
        # Find 'Issue #'.
        if issue_num_text is not '':
            q = q.filter(issue__number=issue_num_text)
    
        # Find 'Publisher'.
        if publisher_text is not '':
            q = q.filter(issue__series__publisher__name__icontains=publisher_text)

        # Find Genre
        #TODO
        
        # Limit publishing years.
        if from_text is not '':
            q = q.filter(issue__series__year_began__gte=int(from_text))
        if to_text is not '':
            q = q.filter(issue__series__year_ended__lte=int(to_text))

        #
        # Filter by store / organization
        q = q.filter(store_id=store_id)
        q = q.filter(organization_id=org_id)

        #
        # Note: Causing a "slice" action forces the database to run the above script.
        return q[:250]
    except Issue.DoesNotExist:
        return None