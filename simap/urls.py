from django.urls import path
from . import views

app_name = 'simap'
urlpatterns = [
    path('index.html', views.index, name='index'),
    path('info.html', views.info, name='info'),
    path('info2.html', views.info2, name='info2'),
    path('wan_IP.html', views.wan_IP, name='wan_IP'),
    path('wan_ping.html', views.wan_ping, name='wan_ping'),
    path('wan_port.html', views.wan_port, name='wan_port'),
    path('lan_IP.html', views.lan_IP, name='lan_IP'),
    path('lan_ping.html', views.lan_ping, name='lan_ping'),
    path('lan_port.html', views.lan_port, name='lan_port'),
    path('wifi_5.html', views.wifi_5, name='wifi_5'),
    path('wifi_24.html', views.wifi_24, name='wifi_24'),
    path('nat_set.html', views.nat_set, name='nat_set'),
    path('nat_lookup.html', views.nat_lookup, name='nat_lookup'),
    path('log.html', views.log, name='log'),

    path('info/cpu-ram', views.cpu_ram, name='cpu_ram'),
]