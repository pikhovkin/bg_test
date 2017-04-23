# coding: utf-8
from django.conf.urls import url

from hr import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mentors$', views.mentors, name='mentors'),
    url(r'^jedi/(?P<pk>[0-9]+)/candidates$', views.view_jedi_candidates, name='view_jedi_candidates'),
    url(r'^jedi/(?P<pk>[0-9]+)/padawan/(?P<candidate_pk>[0-9]+)$', views.view_jedi_padawan, name='view_jedi_padawan'),
    url(r'^candidate/create$', views.create_candidate, name='create_candidate'),
    url(r'^candidate/(?P<pk>[0-9]+)$', views.get_test, name='get_test'),
]
