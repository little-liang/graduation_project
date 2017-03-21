from django.conf.urls import url, include
from hosts import views

'''hosts app的子url '''
urlpatterns = [
    url(r"^$", views.hosts_index, name='hosts'),
    url(r"^host_mgr/$", views.hosts_mgr, name='host_mgr'),
    url(r"^multi_cmd/$", views.multi_cmd, name='multi_cmd'),
    url(r"^submit_task/$", views.submit_task, name='submit_task'),
]
