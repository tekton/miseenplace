from django.conf.urls import *

'''
    these all assume http[s]://URI/api/company/ as the base
'''

urlpatterns = patterns('',
                       # Company interactions
                       url(r'^/current/create', 'recipie.views.api_create_company'),
                       url(r'^/dev/company/create', 'recipie.views.api_create_company'),
                       url(r'^/1.0/company/create', 'recipie.views.api_create_company'),
                       url(r"^/1.0/docs", 'recipie.views.api_default_docs')
                       )
