from django import forms

class CPUForm(forms.Form):
    task_choices = [
        ('gaming_score', 'Gaming'),
        ('productivity_score', 'Productivity'),
        ('blend_score', 'Blend')
    ]

    budget = forms.FloatField(label='Budget', min_value=0)
    task = forms.CharField(label='Task', widget=forms.RadioSelect(choices=task_choices))
    