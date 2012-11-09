# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Named(models.Model):
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class Domain(Named):
    code_name = models.CharField(max_length=500)

class Entry(Named):
    domain = models.ForeignKey(Domain)

class Member(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    user = models.ForeignKey(User, blank=True, null=True)
