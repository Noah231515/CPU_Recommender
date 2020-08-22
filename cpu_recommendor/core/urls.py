from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from core.views import *
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'gpus', views.GPUViewSet)

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('recommendation/', views.Recommendation_Page),
    path(r'^.*', TemplateView.as_view(template_name="home.html"), name="home")
]