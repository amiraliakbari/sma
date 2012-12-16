# -*- coding: utf-8 -*-
import random

from django import template
from django.conf import settings


register = template.Library()

def to_shamsi(date):
    cal = Calverter()
    shamsi = cal.jd_to_jalali(cal.gregorian_to_jd(date.year, date.month, date.day))
    return shamsi

@register.filter
def shamsi_rep(date):
    return '%d/%d/%d' % to_shamsi(date)
