from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Header, HardwareInfo, HardwareField, Lan, Wan
'''
class HeaderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Header
		fields = ('resultCode','resultMessage','isSuccessful')
'''
class MyModelSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		ret = super().to_representation(instance)
		keys = ret.keys()
		for key in keys:
			assert isinstance(key, str)
			if key.find('_') != -1: 
				newKey = key.replace('_', '-')
				ret[newKey] = ret[key]
				del(ret[key])

		return ret

	def to_internal_value(self, data):
		keys = data.keys()
		for key in keys:
			assert isinstance(key, str)
			if key.find('-') != -1: 
				newKey = key.replace('-', '_')
				data[newKey] = data[key]
				del(data[key])

		return super().to_representation(data) 

class MyNestedSerializer(WritableNestedModelSerializer):
	def to_representation(self, instance):
		ret = super().to_representation(instance)
		keys = ret.keys()
		for key in keys:
			assert isinstance(key, str)
			if key.find('_') != -1: 
				newKey = key.replace('_', '-')
				ret[newKey] = ret[key]
				del(ret[key])

		return ret

	def to_internal_value(self, data):
		keys = data.keys()
		for key in keys:
			assert isinstance(key, str)
			if key.find('-') != -1: 
				newKey = key.replace('-', '_')
				data[newKey] = data[key]
				del(data[key])

		return super().to_representation(data) 

class LanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lan
		fields = ('portName', 'portEquip', 'ifOperStatus', 'ifAdminStatus')

class WanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wan
		fields = ('portName', 'portEquip', 'ifOperStatus', 'ifAdminStatus')
		
class HardwareFieldSerializer(WritableNestedModelSerializer):
	lan = LanSerializer(many=True)
	wan = WanSerializer(many=True)

	class Meta:
		model = HardwareField
		fields = ('maxLanPort', 'maxWanPort', 'lan', 'wan')

class HardwareInfoSerializer(MyNestedSerializer):#serializers.ModelSerializer):
	hardware_list = HardwareFieldSerializer(many=False)
#	header = HeaderSerializer()

	class Meta:
		model = HardwareInfo
		fields = ('hardware_list',)#, 'header')
