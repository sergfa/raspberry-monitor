#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
from raspberry.telegram_utils import telegram_bot

import os, sys, configparser, time, logging
from threading import Thread


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

telegram_token = config.get('TELEGRAM', 'token')

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
    time.sleep(checkInterval)    


def exit_clean(signal=None, frame=None):
    logging.info("Temperature monitoring stopping...")
    sys.exit(0)      
        

def bot_get_temperature(bot, update):
    cpuTemp = getCpuTemp()
    gpuTemp = getGpuTemp()
    msg = "Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def bot_get_cpu(bot, update):
    cpuTemp = getCpuTemp()
    msg = "Current CPU temperature: " + str(cpuTemp)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
 
        
def main():	
    logging.info("Temperature monitoring starting...")
    bot_commands = [("get", bot_get_temperature, False),("cpu", bot_get_cpu, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token,'logLevel': loggingLevel, 'commands': bot_commands, 'logFileName': logFileName})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()
    
    monitor_temperature_thread = Thread(name='monitor_temperature', target=checkTemperature)
    monitor_temperature_thread.daemon = True
    monitor_temperature_thread.start()

try:
    main()
    while 1:
            time.sleep(100)
except KeyboardInterrupt:
    exit_clean()
		
