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

def get_task_score(cpu, task):
    return eval(f'cpu.{task}')

def find_best_value_cpu(cpu_list, task):
    max_score = ()

    for cpu in cpu_list:
        adjusted_score = get_task_score(cpu, task) * cpu.value_score
        if not max_score:
            max_score = (cpu.id ,adjusted_score)

        elif adjusted_score >= max_score[1]: #New max is found
            max_score = (cpu.id, adjusted_score)
            
    print(f'Max_score: {max_score}')
    return CPU.objects.get(id=max_score[0])





def Recommendation_Page(request):
    print(request.POST)
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
            performance = [best_for_task[0], best_for_task[1], best_for_task[2]] 

            best_value = find_best_value_cpu(found_cpus.order_by(form.cleaned_data['task']), form.cleaned_data['task'])
            
            return render(request, 'core/recommendation.html', {
                'performance': performance,
                'performance_scores': [get_task_score(cpu, task) for cpu in performance],
                'best_value': best_value,
                'inputs': inputs,
                'task': task_dict[task]
            })

        
    
