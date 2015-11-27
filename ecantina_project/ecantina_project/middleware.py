from django.http import HttpResponseBadRequest, HttpResponseRedirect
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.subdomain import SubDomain


class SubDomainMiddleware(object):
    def process_request(self, request):
        # NGINX must be setup to look like this:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # server_name ~(?<short_url>\w+)\.comicscantina\.com$;
        #
        # ... stuff related to static files here
        # location / {
        #    proxy_set_header X-CustomUrl $short_url;
        #    .... other proxy settings
        # }
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        short_url = request.META.get("HTTP_X_CUSTOMURL")
        
        # Automatically set these variables to be none.
        request.subdomain = None
        request.organization = None
        request.store = None
        
        # If the user is visiting the main site, then exit.
        if short_url is None:
           return None
        short_url = short_url.lower()
        if short_url == "www":
           return None
        
        # Else lookup the company and update the "request" object to include
        # our Store and/or Organization. If the store is "unlisted" then return
        # a 403 error.
        
        try:
            subdomain = SubDomain.objects.get(name=short_url)
            request.subdomain = None
        except SubDomain.DoesNotExist:
            return HttpResponseBadRequest('Company not found')

        if subdomain.organization:
            if subdomain.organization.is_listed is False:
                return HttpResponseRedirect("/403")
            else:
                request.organization = subdomain.organization

        if subdomain.store:
            if subdomain.store.is_listed is False:
                return HttpResponseRedirect("/403")
            else:
                request.store = subdomain.store
        
        return None

# Note:
# http://stackoverflow.com/a/30726090