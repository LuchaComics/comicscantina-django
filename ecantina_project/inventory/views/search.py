import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventory.models.ec.employee import Employee
from inventory.models.gcd.series import Series
from inventory.models.gcd.issue import Issue


@login_required()
def search_series(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                series_text = request.POST['series']
                publisher_text = request.POST['publisher']
                from_text = request.POST['from']
                to_text = request.POST['to']
                series = process_series_search(series_text, publisher_text, from_text, to_text)
            except Series.DoesNotExist:
                series = None
    return render(request, 'inventory/add/master/series.html',{
        'series':series,
    })


def process_series_search(series_text, publisher_text, from_text, to_text):
    q = Series.objects.filter(sort_name__icontains=series_text)
    if publisher_text is not '':
        q = q.filter(publisher__name__icontains=publisher_text)
    if from_text is not '':
        q = q.filter(year_began__gte=int(from_text))
    if to_text is not '':
        q = q.filter(year_ended__lte=int(to_text))

    # Note: Causing a "slice" action forces the database to run the above script.
    return q[:250]


@login_required()
def search_issues(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            series_id = int(request.POST['series_id'])
            publisher_text = request.POST['publisher']
            issue_number_text = request.POST['issue_number']
            issues = process_issues_search(series_id, issue_number_text, publisher_text)
    return render(request, 'inventory/add/master/issue.html',{
        'issues':issues,
    })


def process_issues_search(series_id, issue_number_text, publisher_text):
    try:
        q = Issue.objects.filter(series_id=series_id)
        if issue_number_text is not '':
            q = q.filter(number=issue_number_text)
#    if from_text is not '':
#        q = q.filter(year_began__gte=int(from_text))
#    if to_text is not '':
#        q = q.filter(year_ended__lte=int(to_text))
#    
    # Note: Causing a "slice" action forces the database to run the above script.
        return q[:250]
    except Issue.DoesNotExist:
        return None