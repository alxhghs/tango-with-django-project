# rango/urls.py

from django.conf.urls import url

from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    # having category_name_slug in the url sends it to the matching view
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category,
        name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_page/(?P<category_name_slug>[\w\-]+)/$', views.add_page,
        name='add_page'),
]
