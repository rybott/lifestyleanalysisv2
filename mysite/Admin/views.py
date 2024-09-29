from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import kCalForm

def main(request):
    pass

def login_employee(request):
    return render(request,'login.html',{})

def homepage(request):
    return render(request,'hp.html',{})

