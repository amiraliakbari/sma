# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sma.people.views',
    url(r'^(?:dashboard)$', 'dashboard', name='people/dashboard'),
    url(r'^(?P<domain>.+)/entries/(?:list)$', 'entries_list', name='people/entries-list'),
)
