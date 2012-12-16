# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sma.people.views',
    url(r'^(?:dashboard)?$', 'dashboard', name='people/dashboard'),
    url(r'^(?P<domain>.+)/entries/(?:list)?$', 'entries_list', name='people/entries-list'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/(?:list)?$', 'members_list', name='people/members-list'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/members/(?P<member_id>\d+)/personal$', 'member_view_personal', name='people/member-view-personal'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/members/(?P<member_id>\d+)/educational$', 'member_view_educational', name='people/member-view-educational'),
    url(r'^(?P<domain>.+)/entries/(?P<entry_id>\d+)/members/(?P<member_id>\d+)/sarparasti$', 'member_view_sarparasti', name='people/member-view-sarparasti'),

    url(r'^dictionary$', 'dictionary', name='people/dictionary'),

    url(r'^(?P<domain>.+)/data/import$', 'data_import', name='people/data-import'),
    url(r'^(?P<domain>.+)/data/refine$', 'data_refine', name='people/data-refine'),
)
