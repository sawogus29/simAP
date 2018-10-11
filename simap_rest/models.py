from django.db import models
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


	