from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .forms import kCalForm

def main(request):
    pass

def addkcal(request):
    submitted = False
    if request.method == 'POST':
        form = kCalForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/health/homepage/?submitted=True')
            return HttpResponseRedirect('/health/homepage/')
    else:
        form = kCalForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'Add Cal.html',{'form':form, 'submitted':submitted})