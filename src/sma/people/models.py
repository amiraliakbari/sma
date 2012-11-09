# -*- coding: utf-8 -*-
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Named(models.Model):
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Parented(models.Model):
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

    class Meta:
        abstract = True


class Domain(Named):
    code_name = models.CharField(max_length=500)


class Entry(Named):
    domain = models.ForeignKey(Domain)


class University(Named):
    pass


class FieldCategory(Named, Parented):
    pass


class Field(Named):
    speciality = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(FieldCategory, null=True, blank=True, related_name='fields')

    def __unicode__(self):
        s = self.name
        if self.speciality:
            s += ': ' + self.speciality
        return s


class UniversityRecord(models.Model):
    university = models.ForeignKey(University)
    field = models.ForeignKey(Field, null=True, blank=True)
    student_number = models.CharField(max_length=10, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s: %s [%d تا %d]' % (self.university, self.field, self.start_year, self.end_year)


class Company(Named):
    private = models.BooleanField()


class EmploymentRecord(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True)
    position = models.CharField(max_length=255, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def get_workplace_name(self):
        return unicode(self.company) if self.company else self.description

    def __unicode__(self):
        return u'%s: %s [%d تا %d]' % (self.get_workplace_name(), self.position, self.start_year, self.end_year)


GENDER = (('M', u'مذکر'), ('F', u'مونث'))
MEMBER_IMAGE_UPLOAD_DIR = 'uploads/people/images/'

class Member(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    entry = models.ForeignKey(Entry, related_name='members')

    gender = models.CharField(max_length=2, choices=GENDER)
    birth = models.DateField(null=True, blank=True)
    identification_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT + MEMBER_IMAGE_UPLOAD_DIR, blank=True)
    wife = models.OneToOneField('self', null=True, blank=True, related_name='husband')

    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)

    university_records = models.ManyToManyField(UniversityRecord, blank=True)
    employment_records = models.ManyToManyField(EmploymentRecord, blank=True)

    @property
    def title(self):
        return u'خانم' if self.is_female else u'آقای'

    @property
    def image_url(self):
        mr = settings.MEDIA_ROOT + MEMBER_IMAGE_UPLOAD_DIR
        path = ''
        if not self.image or not self.image.path.startswith(mr):
            if self.is_female:
                path = 'no_image_female.png'
            else:
                path = 'no_image_male.png'
        else:
            path = self.image.path[len(mr):]
        return settings.MEDIA_URL + MEMBER_IMAGE_UPLOAD_DIR + path

    @property
    def is_female(self):
        return self.gender == 'F'

    @property
    def age(self):
        if not self.birth:
            return None
        return (date.today() - self.birth).days / 365

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.first_name, self.last_name)
