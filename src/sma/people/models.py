# -*- coding: utf-8 -*-
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Named(models.Model):
    name = models.CharField(max_length=500, verbose_name=u'نام')

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Parented(models.Model):
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, verbose_name=u'پدر')

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


class EmploymentType(Named):
    pass

class EmploymentRecord(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True)
    position = models.CharField(max_length=255, blank=True)
    employment_type = models.ForeignKey(EmploymentType, verbose_name=u'نوع اشتغال')
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def get_workplace_name(self):
        return unicode(self.company) if self.company else self.description

    def __unicode__(self):
        return u'%s: %s, %s [%d تا %d]' % (self.get_workplace_name(), self.position, self.employment_type, self.start_year, self.end_year)


GENDER = (('M', u'مذکر'), ('F', u'مونث'))
MEMBER_IMAGE_UPLOAD_DIR = 'uploads/people/images/'

class Member(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=500, verbose_name=u'نام')
    last_name = models.CharField(max_length=500, verbose_name=u'نام خانوادگی')
    entry = models.ForeignKey(Entry, related_name='members', verbose_name=u'دوره')

    gender = models.CharField(max_length=2, choices=GENDER, verbose_name=u'جنسیت')
    birth = models.DateField(null=True, blank=True, verbose_name=u'تاریخ تولد')
    identification_number = models.CharField(max_length=20, blank=True, verbose_name=u'کد ملی')
    image = models.FileField(upload_to=settings.MEDIA_ROOT + MEMBER_IMAGE_UPLOAD_DIR, blank=True, verbose_name=u'عکس')
    spouse = models.CharField(max_length = 255, verbose_name=u'همسر', blank=True)

    phone = models.CharField(max_length=20, blank=True, verbose_name=u'تلفن ثابت')
    mobile = models.CharField(max_length=20, blank=True, verbose_name=u'تلفن همراه')

    university_records = models.ManyToManyField(UniversityRecord, blank=True, verbose_name=u'مشخصات تحصیلی')
    employment_records = models.ManyToManyField(EmploymentRecord, blank=True, verbose_name=u'مشخصات شغلی')

    work_status = models.CharField(max_length=100, blank=True, verbose_name=u'وضعیت شغلی')
    university_average = models.CharField(max_length=100, blank=True, verbose_name=u'معدل کل')
    univerity_status = models.CharField(max_length=100, blank=True, verbose_name=u'وضعیت تحصیلی')
    birth_place = models.CharField(max_length=100, blank=True, verbose_name=u'محل تولد')
    father_name = models.CharField(max_length=100, blank=True, verbose_name=u'نام پدر')
    military_service_status = models.CharField(max_length=100, blank=True, verbose_name=u'وضعیت سربازی')
    home_address = models.CharField(max_length=1000, blank=True, verbose_name=u'آدرس محل سکونت')
    parent_address = models.CharField(max_length=1000, blank=True, verbose_name=u'آدرس والدین')
    marriage_status = models.CharField(max_length=100, blank=True, verbose_name=u'وضعیت تاهل')
    marriage_date = models.DateField(null=True, blank=True, verbose_name=u'تاریخ ازدواج')
    admission_status = models.CharField(max_length=100, blank=True, verbose_name=u'وضعیت پذیرش')
    extra_details = models.CharField(max_length=100, blank=True, verbose_name=u'توضیحات')

    raw_data = models.TextField(verbose_name=u'سایر اطلاعات', blank=True)


    @property
    def title(self):
        return u'خانم' if self.is_female else u'آقای'

    @property
    def image_url(self):
        mr = settings.MEDIA_ROOT + MEMBER_IMAGE_UPLOAD_DIR
        path = ''
        if self.image and self.image.path.startswith(MEMBER_IMAGE_UPLOAD_DIR):
            path = self.image.path[len(MEMBER_IMAGE_UPLOAD_DIR)]
        elif not self.image or not self.image.path.startswith(mr):
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

    @property
    def email(self):
        email = self.get_raw_data()[2]
        if email:
            return email
        if self.user:
            return self.user.email
        return None

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.first_name, self.last_name)


    def get_raw_data(self):
        return self.raw_data.split('$$$')


    def set_raw_data(self, data):
        """
            :type data: list
        """
        self.raw_data = '$$$'.join(data)


    @classmethod
    def find_member(cls, first_name=None, last_name=None, stdid=None):
        if stdid:
            try:
                return cls.objects.get(university_records__student_number=stdid)
            except cls.DoesNotExist:
                pass
        if last_name and first_name:
            try:
                return cls.objects.get(first_name=first_name, last_name=last_name)
            except cls.DoesNotExist:
                pass
        return None


class SarparastiProfile(models.Model):
    member = models.OneToOneField(Member, related_name='sarparasti_profile')

    # تحلیل کلی شخصیت
    effective_inputs = models.TextField(verbose_name=u'ورودی‌های اثر گذار', blank=True)
    effective_environments = models.TextField(verbose_name=u'فضاهای ارتباطی اثر گذار', blank=True)
    effective_beliefs = models.TextField(verbose_name=u'باورها، گرایش‌ها و رفتارهای اساسی', blank=True)
    concerns_analysis = models.TextField(verbose_name=u'تحلیل نظام دغدغه‌ها و اولویت‌ها', blank=True)
    final_analysis = models.TextField(verbose_name=u'تحلیل نهایی', blank=True)

    # بعد معرفتی
    knowledge_details = models.TextField(blank=True, verbose_name=u'توضیحات بعد معرفتی')

    # بعد اخلاقی
    dars_akhlagh = models.CharField(max_length=255, blank=True, verbose_name=u'درس اخلاق')
    morabbi_akhlagh = models.CharField(max_length=255, blank=True, verbose_name=u'ارتباط مربی گونه با')
    akhlagh_details = models.TextField(blank=True, verbose_name=u'توضیحات بعد اخلاقی')

    # بعد اجتماعی
    political_activities = models.TextField(blank=True, verbose_name=u'میزان و چگونگی حضور در فضای سیاسی')
    social_details = models.TextField(blank=True, verbose_name=u'توضیحات بعد اجتماعی')

    # بعد حرفه‌ای
    mission = models.TextField(blank=True, verbose_name=u'ماموریت')
    skills = models.TextField(blank=True, verbose_name=u'مهارت‌ها')
    service_pattern = models.TextField(blank=True, verbose_name=u'طرح خدمت')
    service_environment = models.TextField(blank=True, verbose_name=u'شناخت فضای خدمت')
    technical_details = models.TextField(blank=True, verbose_name=u'توضیحات بعد حرفه‌ای')


    @property
    def readings(self):
        user = self.member.user
        if not user:
            return []
        return user.reading_set.all


class DictionaryWord(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'واژه')
    definition = models.TextField(verbose_name=u'تعریف')

    class Meta:
        verbose_name = u'واژه'
        verbose_name_plural = u'واژه‌ها'

    def __unicode__(self):
        return self.name
