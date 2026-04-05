from django.shortcuts import render

def login_page(request):
    return render(request, 'index.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')