# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from sma.people.models import Domain, Entry, Member


def dashboard(request):
    domains = Domain.objects.all()
    return render_to_response('people/dashboard.html', {'domains': domains},
        context_instance=RequestContext(request))


def entries_list(request, domain):
    domain = get_object_or_404(Domain, code_name=domain)
    entries = domain.entry_set.all()
    return render_to_response('people/entries_list.html', {'domain': domain, 'entries': entries},
        context_instance=RequestContext(request))


def members_list(request, domain, entry_id):
    domain_object = Domain.objects.get(code_name=domain)
    entry = get_object_or_404(Entry, domain=domain_object, pk=entry_id)
    members = entry.members.all()
    return render_to_response('people/members_list.html', {'domain': domain_object, 'entry': entry, 'members': members},
        context_instance=RequestContext(request))


def member_view(request, domain, entry_id, member_id):
    try:
        member = Member.objects.select_related().get(pk=member_id, entry__id=entry_id, entry__domain__code_name=domain)
    except Member.DoesNotExist:
        raise Http404()
    return render_to_response('people/member_view.html',
        {'domain': member.entry.domain, 'entry': member.entry, 'member': member},
        context_instance=RequestContext(request))
