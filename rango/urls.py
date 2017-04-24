# rango/urls.py

from django.conf.urls import url

from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/', views.show_category, name='show_category'),
]
