#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
import os, sys, configparsers, time, logging


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'config.cfg'))

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', 'temperature.log')
loggingLevel =  config.get('env', 'loggingLevel')
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(message)s')

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')

cpuThreshold = config.getint('TEMPERATURE_MONITOR', 'cpuThreshold')
gpuThreshold = config.getint('TEMPERATURE_MONITOR', 'gpuThreshold')
checkInterval = config.getint('TEMPERATURE_MONITOR', 'checkInterval')

logging.debug("Temperature monitor module has been started")

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
    logging.debug("Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp))
    if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
        sent = sendTemprature(cpuTemp, gpuTemp);
        msg =  "Email was sent" if sent else "Failed to sent email"	
        logging.debug(msg)
    else:
        pass 
def main():	
    while True:
        checkTemperature()
        time.sleep(checkInterval)

try:
    main()
except:
    logging.critical("Unexpected error:", sys.exc_info()[0])
		
