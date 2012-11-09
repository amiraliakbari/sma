# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from sma.people.models import Domain


def dashboard(request):
    return render_to_response('people/dashboard.html', context_instance=RequestContext(request))

def entries_list(request, domain):
    domain = get_object_or_404(Domain, name=domain)
    entries = domain.entry_set.all()
    return render_to_response('people/entries_list.html', {'entries': entries},
        context_instance=RequestContext(request))
