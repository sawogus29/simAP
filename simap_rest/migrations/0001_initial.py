# Generated by Django 2.1.2 on 2018-10-11 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loggingBufferSize', models.IntegerField()),
                ('loggingServerIpAddr', models.CharField(max_length=50)),
                ('loggingServerPort', models.IntegerField()),
                ('loggingServerProtocol', models.CharField(max_length=50)),
                ('loggingFilename', models.CharField(max_length=50)),
                ('loggingOutputLevel', models.CharField(max_length=50)),
                ('loggingCronLogLevel', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ntp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enableNtpClient', models.BooleanField(default=False)),
                ('provideNtpServer', models.BooleanField(default=False)),
                ('ntpServerCandidates', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simap_rest.Logging')),
                ('ntp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simap_rest.Ntp')),
            ],
        ),
    ]
