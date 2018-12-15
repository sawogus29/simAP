from django.contrib import admin
from django.urls import include, path
import urllib.request
import requests
from django.views.generic import RedirectView
import threading
from simap.views import *
import os
import socket, json

urlpatterns = [
    path('simap/', include('simap.urls')),
    path('v1/', include('simap_rest.urls')),
    path('', RedirectView.as_view(url='/simap/index.html'), name=''),
    path('admin/', admin.site.urls),
    path('system/ram', ram, name='ram'),
    path('system/cpu', cpu, name='cpu'),
    path('life', life, name='life'),
    path('Log_five', Log_five, name='Log_five'),
    path('log/table', table_delete, name='table_delete'),
    path('system/mac-hostname', mac_host, name='mac-hostname'),
    path('wan_IP/IP_address', ip_address, name='ip_address'),
    path('system/ip-netmask-gateway', ip_netmask_gateway, name='ip-netmask-gateway'),
    path('thread1', thread1, name='thread1'),
]

'''
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
'''
'''
print('register to cAPC')
deviceField = {
    "id": '0',
    "name": 'SIMAP',
    "vendorId": 1,
    "vendorName": 'Withus Planet',
    "serialNumber": 'SK_KU_NO2014_312358',
    "type": 1,
    "model": 2,
    "ip": socket.gethostbyname(socket.gethostname()),#get_ip_address(),#socket.gethostbyname(socket.getfqdn()),#netifaces..ifaddresses('{12D26DFF-6CB4-46A6-BB6E-0C41A7961D43}').ip_info[netifaces.AF_INET][0]['addr'],
    "mac": 'sk:ku:0c:74:11:02',
    "userId": 'skku',
    "userPasswd": 'skku',
    "status": 0,
    "mapX": '',
    "mapY": '',
    "counterfeit": True,
    "uptime" : time.ctime(),
    "capabilities" : ['all']
}

CAPC_IP = "capc.withusp.com:7733" # Set destination URL here
res = requests.post('http://' + CAPC_IP + '/v1/devices/registration', data=json.dumps(deviceField)
    , headers = {'Content-Type': 'application/json; charset=utf-8'})
res_dic = res.json()#json.loads(res.text)
print(res_dic)

deviceField = res_dic['devices']
print(deviceField, '\n\n\n-------------')
'''


'''
hostname = socket.gethostname()
mac_addresses = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1]))
wan = urllib.request.urlopen('https://ident.me').read().decode('utf8')
port = 8000
# port = os.environ.get('HOME')
data = {'hostname': hostname, 'mac_addresses': mac_addresses, 'wan_ip': wan, 'port': port}
res = requests.post('http://203.252.34.237:8080/simMe', data=data)


class DBcheck(threading.Thread):
    def run(self):
        b = None
        while 1:
            key = ARP_command.objects.first()
            if key is None:
                continue
            elif b == key.id:
                pass
            else:
                if key.function_num == 1:
                    q = ARP_result(inst="Yes Hello", key=key.id)
                    q.save()
                    q.id
                key.delete()
            b = key.id
            time.sleep(1)


send = DBcheck(name='dbchecking')
send.start()
'''