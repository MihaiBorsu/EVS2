from django.forms import ModelForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import *

class VotingEventForm(ModelForm):
    class Meta:
        model = VotingEvent
        fields = ['event_name',
                  'event_description',
                  'is_public',
                  'enrolled_users'
                  ]

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text'
                  ]

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text'
                  ]









""""
ChoiceFormset = inlineformset_factory(
    Question,Choice,fields=("choice_text",),extra=1)

class BaseQuestionFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseQuestionFormset, self).add_fields(form,index)

        form.nested = ChoiceFormset(
            instance = form.instance,
            data = form.data if form.is_bound else None,
            files = form.files if form.is_bound else None,
            prefix='choice-%s-%s' % (
                form.prefix,
                ChoiceFormset.get_default_prefix()
            )
        )

    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):
        result = super(BaseQuestionFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

QuestionFormset = inlineformset_factory(
    VotingEvent,Question,formset=BaseQuestionFormset,extra=1, fields=("question_text",))

"""
