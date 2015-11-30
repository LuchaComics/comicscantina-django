from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import urllib3
from django.views.decorators.cache import cache_page


def robots_txt_page(request):
    return render(request, 'inventory_base/txt/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'inventory_base/txt/humans.txt', {}, content_type="text/plain")


def comodo_txt_page(request):
    return render(request, 'inventory_base/txt/F860DA3DF4C3F8A7F5EAFFDA1DB33807.txt', {}, content_type="text/plain")


PNG_EXTENSION = 'png'
JPG_EXTENSION = 'jpg'
JPEG_EXTENSION = 'jpeg'
TIFF_EXTENSION = 'tiff'
JFIF_EXTENSION = 'jfif'
GIF_EXTENSION = 'gif'
BMP_EXTENSION = 'bmp'
UNKNOWN_EXTENSION = 'unknown'

PNG_MIMETYPE = 'image/png'
JPEG_MIMETYPE = 'image/jpeg'
BMP_MIMETYPE = 'image/bmp'
TIFF_MIMETYPE = 'image/tiff'
GIF_MIMETYPE = 'image/gif'


def detect_mimetype(url):
    if PNG_EXTENSION in url.lower():
        return PNG_MIMETYPE
        if JPEG_EXTENSION in url.lower():
            return JPEG_MIMETYPE
    if JPG_EXTENSION in url.lower():
        return JPEG_MIMETYPE
        if BMP_EXTENSION in url.lower():
            return BMP_MIMETYPE
    if TIFF_EXTENSION in url.lower():
        return TIFF_MIMETYPE
        if GIF_EXTENSION in url.lower():
            return GIF_MIMETYPE
    return UNKNOWN_EXTENSION


@cache_page(60 * 15)
def image_page(request, filename):
    # Get the image from our comics image database.
    fetch_url = 'http://104.207.135.220/image/'+filename
    http = urllib3.PoolManager()
    r = http.request('GET', fetch_url)
    
    # Return it.
    mimetype = detect_mimetype(filename)
    response = HttpResponse(r.data, content_type=mimetype)
    response['Content-Disposition'] = 'inline; filename="'+filename+'"'
    return response
#/image/741082_1_4.jpg

