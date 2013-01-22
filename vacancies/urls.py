# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from vacancies.views import VacancyList, VacancyPage


urlpatterns = patterns('',
    url('^vacancies/$', VacancyList.as_view(), name='vacancies'),
    url('^vacancies/(?P<pk>[\w-]+)/$', VacancyPage.as_view(), name='vacancy'),
)