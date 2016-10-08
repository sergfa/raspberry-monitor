#Get email alerts when the temperature of Raspberry Pi is too high
---

#Introduction

You can easily be notified by email when the GPU or CPU temperature of you Raspberry Pi is too high (for example if it greater than 75 Celsius ).
#Setup:


Clone project from github

```
git clone https://github.com/sergfa/raspberry-monitor

```

Create config.cfg file from conf-master.cfg within env directory

Update config.cfg.
Replace fromAddrs and password with your gmail address and password, replace toAddrs with address that will recieve email notifications, can be same email address as fromAddrs.
Update cpuTreshold and gpuTrheshold to get email notifications when temperature of Raspberry PI exceeds these thresholds, default values are 75 Celsius.
Default interval to check temperature is 900 seconds (15 minutes), update checkInterval if you want to change it.
Ignore PRESENSE_MONITOR section, this functionality is not working yet.



Run a script from Boot. We're going to use a crontab:

```
 crontab -e
 ```
 
 Pick a text editor and at the bottom of the file, add
 
```
 @reboot export PYTHONPATH=/home/pi/raspberry-monitor; nohup /usr/bin/python3 /home/pi/raspberry-monitor/temprature_monitor/temprature_monitor.py &
```
If you put your project in a different directory, replace /home/pi/raspberry-monitor with the correct path.
Save the file!
 
Reboot Raspberry PI
 
Check if logs are printed in /home/pi/raspberry-monitor/logs/temperature.log file:
    2016-09-30 13:50:54,224 Temperature monitor module has been started
    2016-09-30 13:50:54,305 Current CPU temperature: 58.533, GPU temperature: 58.0

