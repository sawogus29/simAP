from django.shortcuts import render
from django.views import View
from . import models
from . import serializers
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import JsonResponse

class MyJSONRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        header = header = HeaderFactory.getHeader(200, 'Success - ', True)
        data.update(header)
        return super().render(data, *args, **kwargs)

class MyBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, *args, **kwargs):
        header = header = HeaderFactory.getHeader(200, 'Success - ', True)
        data.update(header)
        return super().render(data, *args, **kwargs)

class HeaderFactory:
	def __init__(self):
		pass

	@classmethod
	def getHeader(cls, resultCode, resultMessage, isSuccessful):
		header = { 
			'header' : {
				'resultCode': resultCode,
		        'resultMessage': resultMessage,
		        'isSuccessful': isSuccessful
			}
		}
		
		return header
# Create your views here.

class HealthCheck(View):

    def post(self, request):
    	header = HeaderFactory.getHeader(200, 'Success - alive', True)
    	return JsonResponse(header)

    def get(self, request):
    	header = HeaderFactory.getHeader(200, 'Success - alive', True)
    	res = {**header}
    	return JsonResponse(res)

class MyRetrieveAPIView(generics.RetrieveAPIView):
    pass

class HardwareInfoView(generics.RetrieveUpdateAPIView):
    queryset = models.HardwareInfo.objects.all()
    serializer_class = serializers.HardwareInfoSerializer
    renderer_classes = (MyBrowsableAPIRenderer, MyJSONRenderer, )

class SystemView(View):
    def post(self, request):
    	#TODO : save request body
    	#data = json.load(request.body)
    	#models.System(**data)
    	header = HeaderFactory.getHeader(200, 'Success - system', True)
    	return JsonResponse(header)

    def get(self, request):
    	header = HeaderFactory.getHeader(200, 'Success - system', True)
    	res = {**header}
    	return JsonResponse(res)

class InterfacesView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class VlansView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class DhcpCommonView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class DhcpPoolView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class DhcpStaticView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class ProvisioningView(View):
    def post(self, request):
        header = HeaderFactory.getHeader(200, 'Success - ', True)
        return JsonResponse(header)

class WifiAnalyzerView(View):
    def get(self, request):
        wa = models.WifiAnalyzer()
        data = wa.getScanData()
        header = HeaderFactory.getHeader(200, 'Success - ', True)

        return JsonResponse(data)