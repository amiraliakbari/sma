# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sma.people.views',
    url(r'^(?:dashboard)?$', 'dashboard', name='people/dashboard'),
    url(r'^(?P<domain>.+)/entries/(?:list)?$', 'entries_list', name='people/entries-list'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/(?:list)?$', 'members_list', name='people/members-list'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/members/(?P<member_id>\d+)/?$', 'member_view', name='people/member-view'),
)
