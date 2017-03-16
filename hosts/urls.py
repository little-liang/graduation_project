from django.conf.urls import url, include
from hosts import views

urlpatterns = [
    url(r"^$", views.hosts_index, name='hosts'),
    url(r"^host_mgr/$", views.hosts_mgr, name='host_mgr'),
    url(r"^multi_cmd/$", views.multi_cmd, name='multi_cmd'),
]
