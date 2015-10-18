"""register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', 'recipie.views.user_login_form'),
    url(r'^logout', 'recipie.views.user_logout'),
    url(r'^registration', 'recipie.views.user_registration'),
    url(r"^account/login", 'recipie.views.user_login_form'),
    # company API
    url(r'^api/company', include("recipie.urls")),
    # end company API
    # MainDoc Interactions
    url(r'^api/maindoc/current/create', 'recipie.views.api_create_main_doc'),
    url(r'^api/maindoc/dev/create', 'recipie.views.api_create_main_doc'),
    url(r'^api/maindoc/1.0/create', 'recipie.views.api_create_main_doc'),
    # end MainDoc
    url(r'^default/create', 'recipie.views.process_default_doc'),
    url(r'^default/(.*)/setup.bash', 'recipie.views.morph_default_doc'),
    url(r'^default/(.*)/view', 'recipie.views.view_default_doc'),
    url(r'^default', 'recipie.views.form_default_doc_view'),
    # test react
    url(r'^react', 'recipie.views.index_react'),
    # default_doc
    url(r'^/', 'recipie.views.index'),
    url(r'^', 'recipie.views.index'),
]
