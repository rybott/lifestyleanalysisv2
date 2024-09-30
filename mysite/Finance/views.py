from django.shortcuts import render

def dashboard(request):
    return render(request,'dashboard.html',{})

def categorize(request):
    return render(request,'categorize.html',{})
