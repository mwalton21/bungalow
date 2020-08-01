from django.conf.urls import url
from . import views

app_name = 'zillow'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # API: /zillow/5/
    url(r'^(\d+)/$', views.listing, name='listing'),
    url(r'^(\d+)/sale_history/', views.sale_history, name='sale_history'),
    url(r'^import/$', views.ingest, name='ingest'),
]
