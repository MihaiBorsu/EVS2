# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render, redirect, reverse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import inlineformset_factory

from .models import VotingEvent,Question,Choice
from .forms import *

ChildFormSet = inlineformset_factory(VotingEvent,Question,fields=('question_text',))

class IndexView(generic.ListView):
    template_name = 'voting_index.html'
    queryset = []

    context_object_name = 'Enrolled_Voting_Events'

    def get_queryset(self):
        qs1 = VotingEvent.objects.order_by('-pub_date').filter(owner=self.request.user)
        qs2 = VotingEvent.objects.order_by('-pub_date').filter(enrolled_users=self.request.user)
        return (qs2 | qs1).distinct()


class IndexPublicView(generic.ListView):
    template_name = 'voting_public_index.html'
    queryset = []

    context_object_name = 'Enrolled_Voting_Events'

    def get_queryset(self):
        return  VotingEvent.objects.order_by('-pub_date').filter(is_public=True)

class EventView(generic.DetailView):
    model = VotingEvent
    template_name = 'voting_event_index.html'

    context_object_name = 'event'

    def questions(self):
        return Question.objects.all().filter(voting_event = self.object)

class EventFormView(generic.CreateView):
    template_name = 'createEvent.html'
    form_class = VotingEventForm

    def form_valid(self, form):
        post = form.save(commit = False)
        post.pub_date = timezone.now()
        post.owner = self.request.user
        post.save()
        post.enrolled_users.add(post.owner)
        post.save()
        return super(EventFormView, self).form_valid(form)

    def get_success_url(self):
        #return reverse('add_questions',args=(self.object.id,))
        nxt_url = 'addquestions'+'/'+str(self.object.id)
        return nxt_url

class QuestionView(generic.DeleteView):
    model = Question
    template_name = 'question_index.html'
    context_object_name = 'question'


    def get_object(self, queryset=None):
        return get_object_or_404(Question,
                                 id=self.kwargs['question_id'],
                                 voting_event = self.kwargs['pk'])

    def choices(self):
        return Choice.objects.all().filter(question = self.object)

class QuestinFormView(generic.CreateView):
    template_name = 'addQuestions.html'
    form_class = QuestionForm
    #success_url = '/voting'

    def form_valid(self, form):
        post = form.save(commit=False)
        event_id = self.kwargs['event_id']
        event = get_object_or_404(VotingEvent,id=event_id)
        post.voting_event = event
        post.pub_date = timezone.now()
        post.save()
        return super(QuestinFormView, self).form_valid(form)

    def get_success_url(self):
        return '/voting/addchoices'+'/'+str(self.kwargs['event_id'])+'/'+str(self.object.id)

class ChoiceFormView(generic.CreateView):
    form_class = ChoiceForm
    template_name = 'addChoices.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        question_id = self.kwargs['question_id']
        question = get_object_or_404(Question,id=question_id)
        post.question = question
        post.choice_count = 0
        post.save()
        return super(ChoiceFormView,self).form_valid(form)

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return '/voting/addchoices'+'/'+self.kwargs['event_id']+'/'+self.kwargs['question_id']
        return '/voting/addquestions'+'/'+str(self.kwargs['event_id'])

class ThankyouView(generic.ListView):
    template_name = 'thankyou.html'
    queryset = []

class AlreadyVotedView(generic.ListView):
    template_name = 'already_voted.html'
    queryset = []

class LearnmoreView(generic.ListView):
    template_name = 'learnmore.html'
    queryset = []


def vote (request, question_id,choice_id):  # voting event id to be added
    choice = get_object_or_404(Choice, id=choice_id)
    question = get_object_or_404(Question,id=question_id)

    if not request.user in question.voted_users.all():
        choice.choice_count += 1;
        question.voted_users.add(request.user)
        choice.save()
        question.save()
        return HttpResponseRedirect('/voting/thankyou')
    return HttpResponseRedirect('/voting/alreadyvoted')











"""
def manage_questions(request, pk):
    event = get_object_or_404(VotingEvent, id=pk)

    if request.method == 'POST':
        formset = forms.QuestionFormset(request.POST, instance=event)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('voting:manage_questions', kwargs={"pk": event.id}))
    else:
        formset = forms.QuestionFormset(instance = event)
    return render(request, 'createEvent.html',
                  {'event':event, 'question_formset':formset})
"""
