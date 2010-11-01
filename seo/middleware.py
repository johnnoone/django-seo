# -*- coding: utf-8 -*-

# Copyright 2009 justquick202
# Licenced under MIT Licence
# http://code.google.com/p/django-metatags/
# Adapted by Will Hardy, 2009

from django.db import models

from seo.models import MetaData, update_callback, delete_callback
from seo.utils import get_seo_models

class MetaDataMiddleware(object):
    """
    This middleware adds on the appropriate meta tags into the head
    section of a text/html document
    """
    def process_response(self, request, response):
        # Returns right out if bad status_code or not an text/html document
        if response.status_code != 200 or not \
          response.get('Content-Type','').lower().startswith('text/html'):
            return response
        # Try to get the tag, otherwise just return
        try:
            tag = MetaData.objects.get(path=request.path)
        except MetaData.DoesNotExist:
            return response
        # Parse out the response content
        for i,part in enumerate(response._container):
            # Parse each line of the content
            lines = part.splitlines()
            for j,line in enumerate(lines):
                # Look for first instance of <head>
                if line.find('<head>')>-1:
                    # Insert tags right after the <head> section
                    lines[j] = line.replace('<head>','<head>\n%s'% tag.html)
                    # Pack up the response
                    response._container[i] = '\n'.join(lines)
                    # Return modified response
                    return response
        # Return original response just in case
        return response
	

class AutomaticCreate(object):
	"""plop
	"""
	def __init__(self, arg):
		## Connect the models listed in settings to the update callback.
		for model in get_seo_models():
		    models.signals.post_save.connect(update_callback, sender=model)
		    models.signals.pre_delete.connect(delete_callback, sender=model)

