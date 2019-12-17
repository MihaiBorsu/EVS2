from django.conf.urls import url



from . import views
app_name = 'Voting'

urlpatterns = [
    url(r'^addchoices/(?P<event_id>\d+)/(?P<question_id>\d+)$', view=views.ChoiceFormView.as_view(), name='add_choices'),
    url(r'^addquestions/(?P<event_id>\d+)$', view= views.QuestinFormView.as_view(), name='add_questions'),
    url(r'^$', view = views.IndexView.as_view(), name='voting_index'),
    url(r'^createEvent$', view= views.EventFormView.as_view(), name='create_voting_event'),
    url('(?P<pk>\d+)/(?P<question_id>\d+)/$', view = views.QuestionView.as_view(), name='question_detail'),
    url('(?P<pk>\d+)/$', view = views.EventView.as_view(), name='voting_event_detail'),
    url(r'^public$', view=views.IndexPublicView.as_view(), name='public_voting_events'),
    url(r'^upvote/(?P<question_id>\d+)/(?P<choice_id>\d+)$',views.vote, name='vote'),
    url(r'^alreadyvoted$',view = views.AlreadyVotedView.as_view(), name='already_voted'),
    url(r'^thankyou$',view = views.ThankyouView.as_view(), name='thankyou'),
    url(r'^learnmore$',view = views.LearnmoreView.as_view(), name = 'learn_more')
]

