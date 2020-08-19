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
    image_url = models.URLField(default='')

    gaming_score = models.FloatField(default=0)
    productivity_score = models.FloatField(default=0)
    blend_score = models.FloatField(default=0)
    value_score = models.FloatField(default=0)

class GPU(models.Model):
    name = models.CharField(max_length=100)
    tdp = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    benchmark_score = models.IntegerField(verbose_name='b_score')
    clock_speed = models.FloatField(default=0)
    memory_size = models.FloatField(default=0)
    memory_clock = models.FloatField(default=0)
    directx = models.CharField(max_length=100)

    gaming_score = models.FloatField(default=0)
    productivity_score = models.FloatField(default=0)
    blend_score = models.FloatField(default=0)
    value_score = models.FloatField(default=0)

