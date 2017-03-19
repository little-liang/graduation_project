from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from hosts import models
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
    #这里用的是?select_gid={{ group.id }}
    select_gid = request.GET.get('select_gid')

    #如果这个host_groups 主机组表的id存在，注意这个查询的是host_groups的id
    if select_gid:
        #这里查询的是BindHostToUser，这个与HostGroups有多对多关系，通过__可以查询多对多另一张表的id
        host_list = models.BindHostToUser.objects.filter(host_group__id=select_gid)
    else:
        #有一些用户直接与主机绑定，没有分组，可以弄成未分组
        host_list = request.user.bind_hosts.select_related()
    return render(request, 'hosts/host_mgr.html', {'host_list': host_list})

def multi_cmd(request):
    return render(request, 'hosts/multi_cmd.html')