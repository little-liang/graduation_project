from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def hosts_index(request):
    return render(request, 'hosts/dashboard.html')


def assets_index(request):
    return render(request, 'assets/dashboard.html')


def monitor_index(request):
    return render(request, 'monitor/dashboard.html')
