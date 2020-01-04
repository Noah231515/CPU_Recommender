from django.shortcuts import render
from django.http import HttpResponse
from .models import CPU

# Create your views here.

def test(cpu): #Prolly can use a dataframe for this
    #TESTING FOR PRODUCTION
    if not cpu.boost_clock:
        cpu.boost_clock = 0
    data_list = [
        (cpu.multithreaded_score, 3),
        (cpu.singlethreaded_score, 5),
        (cpu.base_clock, 4),
        (cpu.cores, 3),
        (cpu.boost_clock, 5),
        (100, 3)
    ]
    r_score = 0
    for tup in data_list:
        r_score+= tup[0]*tup[1]
    
    r_score /= 23
    print(f'Recommendation_Score for production tasks {cpu.name}: {r_score} ')
    return r_score

def index(request):
    test_cpu = CPU.objects.get(name='AMD Ryzen 7 3700X')
    test_cpu_2 = CPU.objects.all()[116]

    test(test_cpu)
    test(test_cpu_2)
    return HttpResponse("Hello, world. You're at the polls index.")