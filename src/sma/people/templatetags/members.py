# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from sma.people.models import Member


register = template.Library()

@register.simple_tag
def guess_spouse(member, view_type):
    s = member.spouse
    if not s.strip():
        return ''
    sf = sl = ''
    if ' ' in s:
        sf, sl = s.split(' ', 1)
    spouse = Member.objects.filter(first_name=sf, last_name=sl)
    print 'looking:', sf, '/', sl, len(spouse)
    if len(spouse) != 1:
        return ''
    spouse = spouse[0]
    return u' <a href="%s">(همسر)</a>' % reverse('people/member-view-' + view_type, kwargs={'member_id': spouse.id, 'entry_id': spouse.entry_id, 'domain': spouse.entry.domain.code_name})
