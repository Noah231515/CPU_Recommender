from django.urls import path, include
from django.contrib.auth.models import User
from core.models import GPU
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class GPUSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GPU
        fields = ['name']