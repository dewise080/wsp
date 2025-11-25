from django.shortcuts import render, redirect, get_object_or_404
from custompage.models import customPage
from custompage.forms import customPageForm
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Admin Custom Page Views
class adminCustomPage(LoginRequiredMixin,ListView):
    model = customPage
    template_name = 'dashboard/main/custompage/index.html'
    context_object_name = 'pages'
    extra_context = {'title': 'All Custom Pages'}
    login_url = reverse_lazy('logIn')

class adminCustomPageCreate(LoginRequiredMixin,CreateView):
    model = customPage
    form_class = customPageForm
    template_name = 'dashboard/main/custompage/create.html'
    success_url = reverse_lazy('adminCustomPage')
    extra_context = {'title': 'Create Page'}
    login_url = reverse_lazy('logIn')

    def form_valid(self, form):
        messages.success(self.request, 'Page created successfully!')
        return super().form_valid(form)

class adminCustomPageEdit(LoginRequiredMixin,UpdateView):
    model = customPage
    form_class = customPageForm
    template_name = 'dashboard/main/custompage/edit.html'
    success_url = reverse_lazy('adminCustomPage')
    extra_context = {'title': 'Edit Page'}
    login_url = reverse_lazy('logIn')
    
    def form_valid(self, form):
        messages.success(self.request, 'Page updated successfully!')
        return super().form_valid(form)
    
@login_required(login_url='logIn')
def adminCustomPageDelete(request,id):
    page = get_object_or_404(customPage, id=id)
    messages.warning(request, 'Page deleted successfully!')
    page.delete()
    return redirect('adminCustomPage')

# Custom Page Front
def customPageFront(request, slug):
    page = get_object_or_404(customPage, slug=slug)
    return render(request, 'front/main/partial/custom_page.html', {'page': page})
    
# Error Page
def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def error_500(request):
    return render(request, 'error/500.html', status=500)