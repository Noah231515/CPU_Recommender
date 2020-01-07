from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CPU
from .forms import CPUForm
from django.views import generic
from pandas import DataFrame

# Create your views here.



class IndexView(generic.ListView):
    template_name = 'core/index.html'
    context_object_name = 'cpu_list'
    

    def get_queryset(self):
        return CPU.objects.all()
    
    def get_context_data(self, **kwargs):
        form = CPUForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

def get_cpu_param(cpu, param, modifiers=None):
    if modifiers:
        symbol = modifiers['operation']
        value = modifiers['value']

        return eval(f'cpu.{param}{symbol}{value}')
    else:
        return eval(f'cpu.{param}')


def find_best_three_adjusted_part(cpu_list, task, adjustor, modifiers=None): #Allows to adjust scores, f.ex value and TDP
    adjusted_list = [(cpu, get_cpu_param(cpu, task) * get_cpu_param(cpu, adjustor, modifiers) ) for cpu in cpu_list ]
    top_three = sorted(adjusted_list, key = lambda tup: tup[1], reverse=True)[:3]
    return top_three
    
def Recommendation_Page(request): #Remember, this page depends on the task that the user picks

    if request.method == 'POST':
        form = CPUForm(request.POST)

        if form.is_valid(): #For now we assume for now that there exists valid CPUs at this price
            task_dict = { #could probably pull from form
                'gaming_score': 'Gaming',
                'productivity_score': 'Productivity',
                'blend_score': 'Blend'
            }    
            inputs = form.cleaned_data.copy()
            inputs['task'] = task_dict[ form.cleaned_data['task'] ] #clean this dict a bit with function
            task = form.cleaned_data['task']

            found_cpus = CPU.objects.filter(price__lte=form.cleaned_data['budget'])
            best_for_task = found_cpus.order_by(task).reverse()
            
            performance = best_for_task[:3]
            best_value = find_best_three_adjusted_part(best_for_task, task, 'value_score')
            value_parts = [part[0] for part in best_value]
            
            best_power = find_best_three_adjusted_part(best_for_task, task, 'tdp', modifiers={'operation': '/', 'value': 10})
            power_parts = [part[0] for part in best_power]
            return render(request, 'core/recommendation.html', {
                'best_perf': performance,
                'performance_scores': [get_cpu_param(cpu, task) for cpu in performance],
                'best_value': value_parts,
                'best_power': power_parts,
                'inputs': inputs,
                'task': task_dict[task]
            })

        
    
