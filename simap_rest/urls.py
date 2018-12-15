from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'simap_rest'
urlpatterns = [
    path('keepalive-check', csrf_exempt(views.HealthCheck.as_view())),
    path('configs/system', csrf_exempt(views.SystemView.as_view())),
    path('configs/interfaces', csrf_exempt(views.InterfacesView.as_view())),
    path('configs/vlans', csrf_exempt(views.VlansView.as_view())),
    path('configs/dhcp-dns/common', csrf_exempt(views.DhcpCommonView.as_view())),
    path('configs/dhcp-dns/pool', csrf_exempt(views.DhcpPoolView.as_view())),
    path('configs/dhcp-dns/static-lease', csrf_exempt(views.DhcpStaticView.as_view())),
    path('configs/provisioning-done', csrf_exempt(views.ProvisioningView.as_view())),
    path('wifi-analyzer', csrf_exempt(views.WifiAnalyzerView.as_view())),
    path('infos/hardware-info', csrf_exempt(views.HardwareInfoView.as_view()), kwargs={'pk':'1'}),
]