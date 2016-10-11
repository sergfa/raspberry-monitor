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
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger('temperature')

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')

cpuThreshold = config.getint('TEMPERATURE_MONITOR', 'cpuThreshold')
gpuThreshold = config.getint('TEMPERATURE_MONITOR', 'gpuThreshold')
checkInterval = config.getint('TEMPERATURE_MONITOR', 'checkInterval')

telegram_token = config.get('TEMPERATURE_MONITOR', 'telegram-token')
telegram_bot_password = config.get('TELEGRAM', 'bot-password')


def getCpuTemp():
    temp = 60 if appMode == "dev" else getCpuTemperature()
    return temp
	
def getGpuTemp():
    temp = 60 if appMode == "dev" else getGpuTemperature()
    return temp



def sendTemprature(cpuTemp, gpuTemp):
    text = "Hello,\nCPU temperature is " \
    + str( cpuTemp) + "\nGPU temperature is " +  str(gpuTemp)
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI Temperature Alert",  appMode == "dev")
   

   
def checkTemperature():
    while True:
        cpuTemp = getCpuTemp()
        gpuTemp = getGpuTemp()
        logger.debug("Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp))
        if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
            sent = sendTemprature(cpuTemp, gpuTemp);
            msg =  "Message was sent" if sent else "Failed to sent email"	
            logger.debug(msg)   
        else:
            pass
        time.sleep(checkInterval)    


def exit_clean(signal=None, frame=None):
    logger.info("Temperature monitoring stopping...")
    sys.exit(0)      
        

def bot_get_temperature(bot, update, args):
    if(len(args) < 1):
        update.message.reply_text('Sorry I can not send you data beacuse password is missing, use command /get <password>')
        return
    if(telegram_bot_password != args[0]):
        update.message.reply_text('Sorry I can not send you data beacuse password is incorrect.')
        return   
   
    cpuTemp = getCpuTemp()
    gpuTemp = getGpuTemp()
    msg = "CPU temperature is: " + str(cpuTemp) + ", GPU temperature is: " + str(gpuTemp)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def bot_start(bot, update):
    update.message.reply_text('Hi! This is a private bot, you must have password to use it. Use /get <password> to get data')
    

def main():	
    bot_commands = [("get", bot_get_temperature, True),("start", bot_start, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token, 'commands': bot_commands})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()
    
    monitor_temperature_thread = Thread(name='monitor_temperature', target=checkTemperature)
    monitor_temperature_thread.daemon = True
    monitor_temperature_thread.start()
    
try:
    logger.info("Temperature monitoring starting...")
    time.sleep(120)
    main()
    while 1:
            time.sleep(100)
except KeyboardInterrupt:
    exit_clean()
		
