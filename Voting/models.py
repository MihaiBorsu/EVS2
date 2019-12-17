# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import *
from django.conf import settings


class VotingEvent(models.Model):
    event_name = models.CharField(max_length=200, default="")
    event_description = models.CharField(max_length=1500, default="")
    pub_date = models.DateTimeField('date created', default=timezone.now)
    is_public = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default="",
                              related_name='%(class)s_owner')
    enrolled_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            related_name='%(class)s_enrolled_users')


class Question(models.Model):
    voting_event = models.ForeignKey(VotingEvent, on_delete= models.CASCADE)
    question_text = models.CharField(max_length=1500, default="")
    pub_date = models.DateTimeField('date published', default=timezone.now)
    voted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="%(class)s_voted_users")
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200, default="")
    choice_count = models.IntegerField(default=0)

