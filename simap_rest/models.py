from django.db import models
from wavemon import wavemon
import copy
import json

class Logging(models.Model):
	loggingBufferSize = models.IntegerField()
	loggingServerIpAddr = models.CharField(max_length=50)
	loggingServerPort = models.IntegerField()
	loggingServerProtocol = models.CharField(max_length=50)
	loggingFilename = models.CharField(max_length=50)
	loggingOutputLevel = models.CharField(max_length=50)
	loggingCronLogLevel = models.CharField(max_length=50)


class Ntp(models.Model):
	enableNtpClient = models.BooleanField(default=False)
	provideNtpServer = models.BooleanField(default=False)
	ntpServerCandidates = models.CharField(max_length=200)

class System(models.Model):
	logging = models.ForeignKey(Logging, on_delete=models.CASCADE)
	ntp = models.ForeignKey(Ntp, on_delete=models.CASCADE)



class HardwareField(models.Model):
	maxLanPort = models.IntegerField()
	maxWanPort = models.IntegerField()
	#lan
	#wan
	#hardwareInfo = models.ForeignKey(HardwareInfo, related_name='hardware_list', on_delete=models.CASCADE)

class HardwareInfo(models.Model):
	#hareware-list : Haredware-Field
	#header
	hardware_list = models.ForeignKey(HardwareField, related_name='hardwareInfo', on_delete=models.CASCADE, default=1)
	pass

class HardwareIface(models.Model):
	portName = models.CharField(max_length=50)
	portEquip = models.BooleanField(default=False)
	ifOperStatus = models.BooleanField(default=False)
	ifAdminStatus = models.BooleanField(default=False)

	class Meta:
		abstract = True

	def __str__(self):
		return self.portName + str(self.portEquip) + str(self.ifOperStatus) + str(self.ifAdminStatus)

class Lan(HardwareIface):
	hardwareField = models.ForeignKey(HardwareField, related_name='lan', on_delete=models.CASCADE)
	pass

class Wan(HardwareIface):
	hardwareField = models.ForeignKey(HardwareField, related_name='wan', on_delete=models.CASCADE)
	pass

'''
class Lan(models.Model):
	portName = models.CharField(max_length=50)
	portEquip = models.BooleanField(default=False)
	ifOperStatus = models.BooleanField(default=False)
	ifAdminStatus = models.BooleanField(default=False)
	HardwareField = models.ForeignKey(HardwareField, on_delete=models.CASCADE)

class Wan(models.Model):
	portName = models.CharField(max_length=50)
	portEquip = models.BooleanField(default=False)
	ifOperStatus = models.BooleanField(default=False)
	ifAdminStatus = models.BooleanField(default=False)
	HardwareField = models.ForeignKey(HardwareField, on_delete=models.CASCADE)
'''
class Header(models.Model):
	resultCode = models.IntegerField()
	resultMessage = models.CharField(max_length=50)
	isSuccessful = models.BooleanField(default=True)
	hardwareInfo =  models.ForeignKey('HardwareInfo', on_delete=models.CASCADE)

class WifiAnalyzer():
	def getScanData(self):
		wDict = {}
		apList = []
		result = {}
		w = wavemon.umalloc()
		wavemon.ap_scan(w)

		wDict['entryNum'] = w.entryNum
		wDict['twoGig'] = w.twoGig
		wDict['fiveGig'] = w.fiveGig		

		
		for i in range(w.entryNum):
			apDict = dict([('mac', w.APlist[i].mac), ('essid', w.APlist[i].essid), ('freq',w.APlist[i].freq), ('chan',w.APlist[i].chan) \
			,('has-key', w.APlist[i].has_key), ('last-seen', w.APlist[i].last_seen), ('tsf', w.APlist[i].tsf), ('bss-signal', w.APlist[i].bss_signal) \
			,('bss-signal-qual',w.APlist[i].bss_signal_qual), ('bss-sta-count', w.APlist[i].bss_sta_count), ('bss-chan-usage', w.APlist[i].bss_chan_usage)])

			apList.append(apDict)
		
		wDict['ap-list'] = apList
		result = copy.deepcopy(wDict)
		wavemon.ufree(w)
		#wavemon.terminate()
		return result

		