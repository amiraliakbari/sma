# -*- coding: utf-8 -*-
from django.contrib import admin
from sma.people.models import Entry, Member, Domain, University, UniversityRecord, Company, EmploymentRecord, Field, FieldCategory, DictionaryWord

admin.site.register(Domain)
admin.site.register(Entry)
admin.site.register(Member)
admin.site.register(University)
admin.site.register(UniversityRecord)
admin.site.register(Company)
admin.site.register(EmploymentRecord)
admin.site.register(Field)
admin.site.register(FieldCategory)

admin.site.register(DictionaryWord)
