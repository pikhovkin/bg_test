# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView, TemplateView, CreateView, FormView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
from django.core.urlresolvers import reverse
from django.db.models import Count, QuerySet
from django.db import transaction
from django.conf import settings

from user.roles import USER_ROLE_JEDI, USER_ROLE_CANDIDATE, USER_ROLE_PADAWAN
from models import Test, Question, Answer
from forms import CandidateForm, QuestionForm
from post_service import Message, EMailService


__all__ = (
    'index',
    'mentors',
    'create_candidate',
    'get_test',
    'view_jedi',
    'view_jedi_candidates',
    'view_jedi_padawan',
)


MAX_COUNT_PADAWANS = getattr(settings, 'MAX_COUNT_PADAWANS', 0)


User = get_user_model()


class Index(TemplateView):
    template_name = 'index.html'


class Mentors(ListView):
    model = User
    queryset = model.objects.filter(role=USER_ROLE_JEDI, is_active=True, is_staff=True, is_superuser=False)
    queryset = queryset.annotate(padawans_count=Count('padawans'))
    context_object_name = 'mentors'
    template_name = 'mentors.html'


class CreateCandidate(CreateView):
    form_class = CandidateForm
    template_name = 'create_candidate.html'


class GetTest(FormView):
    model = User
    template_name = 'get_test.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.candidate = User.objects.get(pk=pk)
        self.test = Test.objects.order_by('-created').first()

        return super(GetTest, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GetTest, self).get_form_kwargs()

        kwargs.update({'queryset': self.test.questions.all()})

        return kwargs

    def get_form_class(self):
        return modelformset_factory(Question, form=QuestionForm, extra=0)

    @transaction.atomic
    def form_valid(self, form):
        for f in form.forms:
            answer = Answer(user=self.candidate, question=f.instance, answer=f.cleaned_data['answer'])
            answer.save()

        return super(GetTest, self).form_valid(form)

    @property
    def success_url(self):
        return reverse('index')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(GetTest, self).get_context_data(**kwargs)

        test = Test.objects.order_by('-created').first()
        context['test'] = test

        return context


class ViewJediCandidates(DetailView):
    model = User
    template_name = 'view_jedi_candidates.html'

    def get_context_data(self, **kwargs):
        context = super(ViewJediCandidates, self).get_context_data(**kwargs)

        jedi = context['object']

        users = User.objects.filter(planet=jedi.planet, role=USER_ROLE_CANDIDATE)
        users = users.annotate(answers_count=Count('answers')).filter(answers_count__gt=0)

        context['candidates'] = users

        return context


class ViewJediPadawan(ListView):
    model = User
    template_name = 'view_candidate_answers.html'
    context_object_name = 'answers'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.jedi = User.objects.get(pk=pk)

        candidate_pk = self.kwargs.get('candidate_pk')
        self.candidate = User.objects.get(pk=candidate_pk)

        self.test = Test.objects.order_by('-created').first()

        return super(ViewJediPadawan, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        answers = Answer.objects.filter(user=self.candidate, question__test=self.test)

        return answers

    @property
    def success_text(self):
        text = '{}, вы успешно прошли испытание и зачислены в падаваны к джедаю {}!'
        return text.format(self.candidate.username, self.jedi.username)

    def post(self, request, *args, **kwargs):
        if MAX_COUNT_PADAWANS and User.objects.filter(mentor=self.jedi).count() >= MAX_COUNT_PADAWANS:
            self.object_list = self.get_queryset()

            error = 'Джедай {} больше не может брать себе падаванов в обучение!'.format(self.jedi)

            return self.render_to_response(self.get_context_data(error=error))

        self.candidate.mentor = self.jedi
        self.candidate.role = USER_ROLE_PADAWAN
        self.candidate.save()

        service = EMailService()
        message = Message(self.success_text, service)
        message.send()

        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(ViewJediPadawan, self).get_context_data(**kwargs)

        context['jedi'] = self.jedi
        context['test'] = self.test

        return context


index = Index.as_view()
mentors = Mentors.as_view()
create_candidate = CreateCandidate.as_view()
get_test = GetTest.as_view()
view_jedi_candidates = ViewJediCandidates.as_view()
view_jedi_padawan = ViewJediPadawan.as_view()
