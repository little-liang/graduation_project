from django.conf.urls import url, include
from hosts import views

urlpatterns = [
    url(r"^$", views.hosts_index, name='hosts')
]
