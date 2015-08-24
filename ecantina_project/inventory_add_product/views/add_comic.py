import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.gcd.issue import Issue
from api.models.gcd.story import GCDStory
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from inventory_add_product.forms import IssueForm
from inventory_add_product.forms import ComicForm
from inventory_add_product.forms import ImageUploadForm
from inventory_add_product.forms import ProductForm


@login_required(login_url='/inventory/login')
def comic_page(request, org_id, store_id, issue_id, comic_id):
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
    try:
        story = GCDStory.objects.filter(issue_id=issue_id)[:1]
    except GCDStory.DoesNotExist:
        story = None

    # Generate Forms
    imageupload_form = ImageUploadForm()

    try:
        comic = Comic.objects.get(comic_id=comic_id)
        comic_form = ComicForm(instance=comic)
        product_form = ProductForm(instance=comic.product)
    except Comic.DoesNotExist:
        comic_form = ComicForm()
        product_form = ProductForm()

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
    return render(request, 'inventory_add_product/comic/add/view.html',{
        'org': org,
        'store': store,
        'issue': issue,
        'tab':'add',
        'imageupload_form': imageupload_form,
        'product_form': product_form,
        'comic_form': comic_form,
        'issue_form': issue_form,
        'employee': Employee.objects.get(user=request.user),
        'locations': Store.objects.filter(organization_id=org_id),
        'local_css_library':settings.INVENTORY_CSS_LIBRARY,
        'local_js_library_header':settings.INVENTORY_JS_LIBRARY_HEADER,
        'local_js_library_body':settings.INVENTORY_JS_LIBRARY_BODY,
    })


@login_required()
def list_products(request, org_id, store_id, issue_id):
    comics = {'status' : 'failed', 'message' : 'unknown error detected.'}
    products = None
    if request.is_ajax():
        if request.method == 'POST':
            try:
                comics = Comic.objects.filter(issue_id=issue_id)
            except Comic.DoesNotExist:
                comics = None
    return render(request, 'inventory_add_product/comic/add/list.html',{
        'comics': comics,
        'org_id':org_id,
        'store_id':store_id,
        'issue_id':issue_id,
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
            # Step (1): Find the comic
            try:
                comic_id = request.POST['comic_id']
                comic = None
                if comic_id is not '':
                    comic = Comic.objects.get(comic_id=int(comic_id))
            except Comic.DoesNotExist:
                comic = None
            
            # Step (2): Find/Make a product
            if comic is None:
                product_form = ProductForm(request.POST, request.FILES)
            else:
                product_form = ProductForm(request.POST, request.FILES, instance=comic.product)
            product_form.instance.organization_id = org_id
            if product_form.is_valid():
                product_form.save()
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(product_form.errors)}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            
            # Step (3): Find the product to edit, else load new model into database.
            form = ComicForm(request.POST, request.FILES, instance=comic)
        
            # Step (4): Attach "cover" image if one was uploaded previously.
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
            
            # Step (5): Attach "issue" object.
            try:
                issue = Issue.objects.get(issue_id=issue_id)
                form.instance.issue = issue
            except Issue.DoesNotExist:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : 'could not find issue',
                }), content_type="application/json")

            # Step (6): Validate the form.
            form.instance.product = product_form.instance
            if form.is_valid():
                # Step (7): Save & return OK status.
                form.save()
                
                # Step (8) Return success status.
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
    sections = None
    if request.is_ajax():
        if request.method == 'POST':
            try:
                sections = Section.objects.filter(store_id=this_store_id)
            except Section.DoesNotExist:
                sections = None
    return render(request, 'inventory_add_product/comic/add/section_dropdown.html',{
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
                    'message' : 'deleted',
                }
            except Comic.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")