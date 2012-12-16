# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from sma.people.forms import SarparastiProfileForm
from sma.people.models import Domain, Entry, Member, SarparastiProfile, DictionaryWord


def dashboard(request):
    domains = Domain.objects.all()
    return render_to_response('people/dashboard.html', {'domains': domains},
        context_instance=RequestContext(request))


def dictionary(request):
    domains = Domain.objects.all()
    words = {}
    for word in DictionaryWord.objects.all().order_by('name'):
        letter = word.name[0]
        if not letter in words:
            words[letter] = []
        words[letter].append(word)

    return render_to_response('people/dictionary.html', {'domains': domains, 'words': words},
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


def member_view_personal(request, domain, entry_id, member_id):
    try:
        member = Member.objects.select_related().get(pk=member_id, entry__id=entry_id, entry__domain__code_name=domain)
    except Member.DoesNotExist:
        raise Http404()

    member.unr = filter(lambda s: s.strip() != '', member.get_raw_data()[3:6])
    return render_to_response('people/member_view_personal.html',
        {'domain': member.entry.domain, 'entry': member.entry, 'member': member},
        context_instance=RequestContext(request))


def member_view_educational(request, domain, entry_id, member_id):
    try:
        member = Member.objects.select_related().get(pk=member_id, entry__id=entry_id, entry__domain__code_name=domain)
    except Member.DoesNotExist:
        raise Http404()

    member.unr = filter(lambda s: s.strip() != '', member.get_raw_data()[3:6])
    return render_to_response('people/member_view_educational.html',
        {'domain': member.entry.domain, 'entry': member.entry, 'member': member},
        context_instance=RequestContext(request))


def member_view_sarparasti(request, domain, entry_id, member_id):
    try:
        member = Member.objects.select_related().get(pk=member_id, entry__id=entry_id, entry__domain__code_name=domain)
    except Member.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        form = SarparastiProfileForm(request.POST, instance=member.sarparasti_profile)
        if form.is_valid():
            form.save()
    else:
        form = SarparastiProfileForm(instance=member.sarparasti_profile)

    return render_to_response('people/member_view_sarparasti.html',
        {'domain': member.entry.domain, 'entry': member.entry, 'member': member, 'form': form},
        context_instance=RequestContext(request))


def data_import(request, domain):
    domain = get_object_or_404(Domain, code_name=domain)

    if request.method == 'POST':
        a = request.POST['data'].split('\r\n')
        a = [x.split('\t') for x in a]
        msg = []
        st = {'good': 0, 'bad': 0, 'failed': 0}
        for row in a:
            try:
                m = Member.find_member(first_name=row[1], last_name=row[2], stdid=row[3])
                if m:
                    msg.append(u'هشدار: ‍`%s %s‍` تکراری است، اطلاعات قبلی به روز خواهد شد.' % (row[1], row[2]))
                    st['bad'] += 1
                else:
                    m = Member()

                raw = []

                m.first_name = row[1]
                m.last_name = row[2]
                raw.append(row[3]) #stdid
                raw.append(row[4]) #field
                m.university_average = row[5]
                m.mobile = row[6]
                raw.append(row[7]) #email
                m.marriage_status = row[9]
                raw.append(row[10]) #کارشناسی
                raw.append(row[11]) #ارشد
                raw.append(row[12]) #دکتری
                m.univerity_status = row[13]
                m.work_status = row[14]
                m.home_address = row[15]
                m.parent_address = row[16]
                m.spouse = row[17]
                m.admission_status = row[18]
                m.extra_details = row[19]
                m.set_raw_data(raw)

                if not row[8]:
                    row[8] = '0'
                assert row[0] in ['1', '2']
                assert row[8] in ['0', '1']
                m.entry_id = int(row[8]) + 2*(int(row[0])-1)

                m.save()
                st['good'] += 1
            except Exception as e:
                print e
                st['failed'] += 1
        msg.append('=' * 55)
        msg.append(u'%(good)d ردیف بدون مشکل و %(bad)d ردیف با مشکل جزیی وارد سیستم شد. %(failed)d ردیف هم به دلیل خطا قابل فهم برای سیستم نبود.' % st)
        return HttpResponse(u'<body style="direction: rtl"><h2>داده‌ها وارد شدند</h2><div><ul>%s</ul></div></body>' % '\n'.join(['<li>%s</li>' % m for m in msg]))

    return render_to_response('people/data_import.html', {'domain': domain},
        context_instance=RequestContext(request))


def data_refine(request, domain):
    domain = get_object_or_404(Domain, code_name=domain)

    members = Member.objects.all()
    for m in members:

#        # Detecting gender by entry
#        m.gender = 'F' if (m.entry_id % 2 == 1) else 'M'

#        # Creating user for members
#        if m.user is None:
#            m.user = User.objects.create(username='member-%d' % m.pk, first_name=m.first_name, last_name=m.last_name, password='')

#        # Creating sarparasti profile for members for the first time
#        m.sarparasti_profile = SarparastiProfile.objects.create(member=m)
#        m.save()

#        # User Email Extraction
#        m.user.email = m.email
#        m.user.save()

        m.save()

    return HttpResponse('<html><body><h2>OK!</h2></body></html>')
