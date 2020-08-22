from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from core.views import *

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('recommendation/', views.Recommendation_Page),
    path(r'^.*', TemplateView.as_view(template_name="home.html"), name="home")
]