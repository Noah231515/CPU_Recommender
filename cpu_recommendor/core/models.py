from django.db import models

# Create your models here.
class CPU(models.Model):
    name = models.CharField(max_length=100)
    socket = models.CharField(max_length=100)
    multithreaded_score = models.IntegerField(verbose_name='m_score')
    singlethreaded_score = models.IntegerField(verbose_name='s_score')
    samples = models.IntegerField()
    release_date = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    brand =  models.CharField(max_length=100)
    model =  models.CharField(max_length=100)
    cores = models.IntegerField(default=0)
    base_clock = models.FloatField(default=0)
    boost_clock = models.FloatField(default=0)
    multithreading = models.BooleanField(default=False)
    tdp = models.IntegerField(default=0)
    integrated_graphics = models.CharField(max_length=100, default='', null=True)
