#!/usr/bin/env python3
from raspberry.gmail_utils import sendEmail
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
from raspberry.telegram_utils import is_logged_in
import os, sys, configparser, time, logging
from threading import Thread

logger = logging.getLogger('temperature')

def getCpuTemp():
    temp = getCpuTemperature()
    return temp
	
def getGpuTemp():
    temp = getGpuTemperature()
    return temp

def sendTemprature(cpuTemp, gpuTemp, config):
    appMode = config.get('env', 'mode')
    gmailFromAddr = config.get('gmail', 'fromAddrs')
    gmailPassword= config.get('gmail', 'password')
    gmailToAddr = config.get('gmail', 'toAddrs')
    text = "Hello,\nCPU temperature is " \
    + str( cpuTemp) + "\nGPU temperature is " +  str(gpuTemp)
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI Temperature Alert",  appMode == "dev")
   
def checkTemp(config):
    cpuThreshold = config.getint('TEMPERATURE_MONITOR', 'cpuThreshold')
    gpuThreshold = config.getint('TEMPERATURE_MONITOR', 'gpuThreshold')
    checkInterval = config.getint('TEMPERATURE_MONITOR', 'checkInterval')

    while True:
        cpuTemp = getCpuTemp()
        gpuTemp = getGpuTemp()
        logger.debug("Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp))
        if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
            sent = sendTemprature(cpuTemp, gpuTemp, config);
            msg =  "Message was sent" if sent else "Failed to sent email"	
            logger.debug(msg)   
        else:
            pass
        time.sleep(checkInterval)    
        
def bot_get_temperature(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    cpuTemp = getCpuTemp()
    gpuTemp = getGpuTemp()
    msg = "CPU temperature is: " + str(cpuTemp) + ", GPU temperature is: " + str(gpuTemp)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    
		
