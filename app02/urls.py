from django.conf.urls import url
from app02 import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^aaa/', views.aaa, name='aaa'),
]