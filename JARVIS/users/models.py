from __future__ import unicode_literals

from django.db import models


class ExtendedUser(models.Model):
    user = models.OneToOneField('auth.User')
    priority = models.PositiveIntegerField(default=1)
    team = models.ForeignKey('Team', blank=True, null=True)


class Team(models.Model):
    name = models.CharField(max_length=255)
