# -*- coding: utf-8 -*-
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


class Author(Named):
    class Meta:
        verbose_name = u'نویسنده'
        verbose_name_plural = u'نویسنده‌ها'


class Publisher(Named):
    class Meta:
        verbose_name = u'ناشر'
        verbose_name_plural = u'ناشران'


class BookCategory(Named, Parented):
    class Meta:
        verbose_name = u'دسته‌ی موضوعی'
        verbose_name_plural = u'دسته‌های موضوعی'


class BookType(Named):
    class Meta:
        verbose_name = u'نوع منبع'
        verbose_name_plural = u'نوع‌های منبع'


class Book(models.Model):
    author = models.ForeignKey(Author, blank=True, null=True, verbose_name=u'نویسنده')
    other_authors = models.ManyToManyField(Author, related_name='+', blank=True, verbose_name=u'سایر نویسندگان')
    type = models.ForeignKey(BookType, verbose_name=u'نوع')
    publisher = models.ForeignKey(Publisher, blank=True, null=True, verbose_name=u'ناشر')
    name = models.CharField(max_length=255, verbose_name=u'عنوان')
    sub_title = models.CharField(max_length=255, blank=True, verbose_name=u'عنوان فرعی')
    pages = models.IntegerField(blank=True, null=True, verbose_name=u'تعداد صفحات')
    price = models.IntegerField(blank=True, null=True, verbose_name=u'قیمت')
    categories = models.ManyToManyField(BookCategory, blank=True, verbose_name=u'دسته‌بندی موضوعی')

    class Meta:
        verbose_name = u'کتاب'
        verbose_name_plural = u'کتاب‌ها'

    def __unicode__(self):
        return '%s %s (%s)' % (unicode(self.type), self.name, unicode(self.author))


class Reading(models.Model):
    book = models.ForeignKey(Book, verbose_name=u'کتاب')
    user = models.ForeignKey(User, verbose_name=u'کاربر')
    subject = models.CharField(max_length=255, verbose_name=u'موضوع')
    percent_read = models.IntegerField(blank=True, null=True, verbose_name=u'درصد خوانده شده')
    reading_start = models.DateField(blank=True, null=True, verbose_name=u'شروع خواندن')
    reading_end = models.DateField(blank=True, null=True, verbose_name=u'اتمام خواندن')
    review = models.TextField(blank=True, verbose_name=u'نظر')

    class Meta:
        verbose_name = u'کتاب خوانده شده'
        verbose_name_plural = u'کتاب‌های خوانده شده'

    def __unicode__(self):
        return u'%s %s، خوانده شده توسط %s (%%%s)' % (self.book.type, self.book.name, self.user.get_full_name(), unicode(self.percent_read) if self.percent_read else '?')
