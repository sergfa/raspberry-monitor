#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
import os

import configparser
import time

config = configparser.ConfigParser()
#config.read('env/config.cfg')
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'config.cfg'))

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')

cpuThreshold = config.getint('TEMPERATURE_MONITOR', 'cpuThreshold')
gpuThreshold = config.getint('TEMPERATURE_MONITOR', 'gpuThreshold')
checkInterval = config.getint('TEMPERATURE_MONITOR', 'checkInterval')

def getCpuTemp():
    temp = 60 if appMode == "dev" else getCpuTemperature()
    return temp
	
def getGpuTemp():
    temp = 60 if appMode == "dev" else getGpuTemperature()
    return temp



def sendTemprature(cpuTemp, gpuTemp):
    text = "Hello,\n\nCPU temperature is " \
    + str( cpuTemp) + "\nGPU temperature is " +  str(gpuTemp)
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI Temperature Alert",  appMode == "dev")
   

   
def checkTemperature():
    cpuTemp = getCpuTemp()
    gpuTemp = getGpuTemp()
    print("CPU temperature: " + str(cpuTemp), ", GPU temperature: " + str(gpuTemp))
    if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
        sent = sendTemprature(cpuTemp, gpuTemp);
        msg =  "Email was sent" if sent else "Failed to sent email"	
        print(msg)
    else:
        pass 
	
while True:
    checkTemperature()
    time.sleep(checkInterval)   
		