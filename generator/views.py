from django.shortcuts import render
from .forms import ResumeForm
from .utils import extract_resume_data

def resume_builder(request):
    data = None
    selected_template = "template1"
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['experience_text']
            selected_template = form.cleaned_data['template_choice']
            data = extract_resume_data(user_text)
    else:
        form = ResumeForm()

    return render(request, 'generator/dashboard.html', {
        'form': form,
        'data': data,
        'template': selected_template,
    })
