# -*- coding: utf-8 -*-
import random

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def static(path):
    return settings.STATIC_URL + path


@register.simple_tag
def css(path):
    long_form = True
    if not path.endswith('.css'):
        path += '.css'
        long_form = False
    path = '%s?%d' % (path, random.randrange(10000, 99999))
    return '<link rel="stylesheet" href="%s%s%s" type="text/css" />' % (
        settings.STATIC_URL, '' if long_form else 'css/', path)


@register.simple_tag
def js(path):
    if not path.endswith('.js'): path = 'js/' + path + '.js'
    path = '%s?%d' % (path, random.randrange(10000, 99999))
    return '<script type="text/javascript" src="%s%s"></script>' % (settings.STATIC_URL, path)

@register.filter
def field(form, field_name):
    f = form.fields[field_name]
    err = f.errors if hasattr(f, 'errors') else ''
    return mark_safe(u'%s: %s %s' %(f.label, f.widget.render('n', f.get_value()), err))
