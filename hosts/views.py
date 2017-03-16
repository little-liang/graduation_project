from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required()
def index(request):
    return render(request, "index.html")

@login_required()
def hosts_index(request):
    return render(request, 'hosts/dashboard.html')

@login_required()
def assets_index(request):
    return render(request, 'assets/dashboard.html')

@login_required()
def monitor_index(request):
    return render(request, 'monitor/dashboard.html')

def acc_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return HttpResponseRedirect("/")
        else:
            login_err = 'Wrong username or password!'

    return render(request, 'login.html', {'login_err': login_err})

@login_required()
def acc_logout(request):
    logout(request)

    return HttpResponseRedirect("/")


def hosts_mgr(request):
    return render(request, 'hosts/host_mgr.html')

def multi_cmd(request):
    return render(request, 'hosts/multi_cmd.html')