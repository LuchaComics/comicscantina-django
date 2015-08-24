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
from inventory_add_product.forms import IssueForm


@login_required(login_url='/inventory/login')
def search_comics_page(request, org_id, store_id):
    return render(request, 'inventory_add_product/comic/search/search.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'add',
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
            issues = find_issues(
                series_text,
                issue_num_text,
                publisher_text,
                genre_text,
                from_text,
                to_text
            )
    return render(request, 'inventory_add_product/comic/search/search_results.html',{
        'issues' : issues,
    })


def find_issues(series_text, issue_num_text, publisher_text, genre_text, from_text, to_text):
    try:
        # Lookup 'Series'.
        q = GCDIssue.objects.filter(series__sort_name__icontains=series_text)
        
        # Find 'Issue #'.
        if issue_num_text is not '':
            q = q.filter(number=issue_num_text)
        
        # Find 'Publisher'.
        if publisher_text is not '':
            q = q.filter(series__publisher__name__icontains=publisher_text)

        # Find Genre
        #TODO
        
        # Limit publishing years.
        if from_text is not '':
            q = q.filter(series__year_began__gte=int(from_text))
        if to_text is not '':
            q = q.filter(series__year_ended__lte=int(to_text))

        #
        # Group by Series
        q.query.group_by = ['series_id']

        #
        # Note: Causing a "slice" action forces the database to run the above script.
        return q[:250]
    except GCDIssue.DoesNotExist:
        return None