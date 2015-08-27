from django.shortcuts import render


def robots_txt_page(request):
    return render(request, 'inventory_base/txt/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'inventory_base/txt/humans.txt', {}, content_type="text/plain")
