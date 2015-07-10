import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inventory.models.gcd.issue import Issue
from inventory.models.gcd.story import Story
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.organization import Organization
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.section import Section
from inventory.models.ec.comic import Comic
from inventory.forms.issueform import IssueForm
from inventory.forms.comicform import ComicForm
from inventory.forms.imageuploadform import ImageUploadForm


@login_required(login_url='/inventory/login')
def add_product_page(request, org_id, store_id, issue_id):
    org = Organization.objects.get(org_id=org_id)
    employee = Employee.objects.get(user=request.user)
    store = Store.objects.get(store_id=store_id)
    stores = Store.objects.filter(organization=org)
    try:
        sections = Section.objects.filter(store=store)
    except Section.DoesNotExist:
        sections = None
    try:
        issue = Issue.objects.get(issue_id=issue_id)
    except Issue.DoesNotExist:
        issue = None
#    try:
#        story = Story.objects.get(issue_id=issue_id)
#    except Story.DoesNotExist:
#        story = None

    # Generate Forms
    imageupload_form = ImageUploadForm()
    
    product_form = ComicForm()

    issue_form = IssueForm(initial={
        'series': issue.series,
        'number': issue.number,
        'title': issue.title,
        'publisher': issue.series.publisher,
    })

    # Update forms
#    if story is not None:
#        issue_form.fields['genre'].initial = story.genre
    if stores is not None:
        # http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
        product_form.fields["store"].queryset = stores
    if sections is not None:
        product_form.fields["section"].queryset = sections

    # Render page
    return render(request, 'inventory/add_inventory/comic/add/view.html',{
        'org': org,
        'store': store,
        'issue': issue,
        'tab':'add',
        'imageupload_form': imageupload_form,
        'product_form': product_form,
        'issue_form': issue_form,
        'employee': Employee.objects.get(user=request.user),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def list_products(request, org_id, store_id, issue_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error detected.'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                products = Comic.objects.filter(issue_id=issue_id)
            except Product.DoesNotExist:
                products = None
    return render(request, 'inventory/add_inventory/comic/add/list.html',{
        'products': products,
    })


@login_required()
def ajax_save_uploaded_cover(request, org_id, store_id, issue_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                response_data = {
                    'status' : 'success',
                    'message' : 'saved',
                    'src': form.instance.image.url,
                    'id': form.instance.upload_id,
                }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_add_product(request, org_id, store_id, issue_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = ComicForm(request.POST, request.FILES)
            
            # Step (1): Attach "store", "organization", & "section" object.
            form.instance.organization = Organization.objects.get(org_id=org_id)
            this_store_id = form['store'].value()
            if this_store_id is not '':
                form.instance.store = Store.objects.get(store_id=int(this_store_id))

            this_section_id = form['section'].value()
            if this_section_id is not '':
                form.instance.section = Section.objects.get(section_id=int(this_section_id))
        
            # Step (2): Attach "cover" image if one was uploaded previously.
            upload_id = request.POST['upload_id']
            cover = None
            if upload_id is not '':
                try:
                    cover = ImageUpload.objects.get(upload_id=int(upload_id))
                    cover.is_assigned = True
                    cover.save()
                    form.instance.cover = cover
                except ImageUpload.DoesNotExist:
                    pass
            
            # Step (3): Attach "issue" object.
            try:
                issue = Issue.objects.get(issue_id=issue_id)
                form.instance.issue = issue
            except Issue.DoesNotExist:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : 'could not find issue',
                }), content_type="application/json")

            # Step (4): Validate the form.
            if form.is_valid():
                # Step (5): Save & return OK status.
                form.save()
                response_data = {
                    'status' : 'success',
                    'message' : 'saved',
                }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_sections_per_store(request, org_id, store_id, issue_id, this_store_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error detected.'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                sections = Section.objects.filter(store_id=this_store_id)
            except Section.DoesNotExist:
                sections = None
    return render(request, 'inventory/add_inventory/comic/add/section_dropdown.html',{
        'sections': sections,
    })


@login_required()
def ajax_delete_comic(request, org_id, store_id, issue_id, comic_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                comic = Comic.objects.get(comic_id=comic_id)
                comic.delete()
                response_data = {
                    'status' : 'success',
                    'message' : 'saved',
                }
            except Comic.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")