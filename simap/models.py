from django.db import models

# Create your models here.

class Log(models.Model):
    time = models.DateTimeField('date published')
    cpu = models.IntegerField()
    ram = models.IntegerField()
    check = models.BooleanField(default=True)

class ARP_command(models.Model):
    function_num = models.IntegerField()
    jason = models.TextField()

class ARP_result(models.Model):
    inst = models.TextField()
    key = models.IntegerField()

class RAM(models.Model):
    memory = models.FloatField()

class CPU(models.Model):
    CPU = models.FloatField()

class IP(models.Model):
    IP = models.CharField(max_length=50)
