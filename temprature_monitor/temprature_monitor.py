#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
from raspberry.telegram_utils import telegram_bot
from raspberry.telegram_utils import get_telegram_state

import telegram

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
    text = "Hello,\nCPU temperature is " \
    + str( cpuTemp) + "\nGPU temperature is " +  str(gpuTemp)
    if(telegram_send_message(text)):
        return True
    else:    
        return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI Temperature Alert",  appMode == "dev")
   

   
def checkTemperature():
    while True:
        cpuTemp = getCpuTemp()
        gpuTemp = getGpuTemp()
        logging.debug("Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp))
        if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
            sent = sendTemprature(cpuTemp, gpuTemp);
            msg =  "Message was sent" if sent else "Failed to sent email"	
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
  
def telegram_send_message(message):
    state = get_telegram_state()
    if(state["status"] != "enabled"):
        logging.info('Cannot send message: "%s" because bot is not enabled' % message)
        return False
        
    try:
        bot.sendMessage(chat_id=state["chat_id"], parse_mode='Markdown', text=message, timeout=10)
    except Exception as e:
        logging.error('Telegram message failed to send message "%s" with exception: %s' % (message, e))
    else:
        logging.info('Telegram message Sent: "%s"' % message)
        return True
 

def main():	
    logging.info("Temperature monitoring starting...")
    bot_commands = [("get", bot_get_temperature, False),("cpu", bot_get_cpu, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token, 'commands': bot_commands, 'logging': logging})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()
    
    monitor_temperature_thread = Thread(name='monitor_temperature', target=checkTemperature)
    monitor_temperature_thread.daemon = True
    monitor_temperature_thread.start()
    
try:
    time.sleep(120)
    bot = telegram.Bot(token=telegram_token)
    main()
    while 1:
            time.sleep(100)
except KeyboardInterrupt:
    exit_clean()
		
