#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.ip_utils import getPublicIP

import os, sys, configparser, time, logging, datetime
from threading import Thread

from raspberry.telegram_utils import telegram_bot
from raspberry.telegram_utils import telegram_send_message


import telegram


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'config.cfg'))

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', 'my_ip.log')
loggingLevel =  config.get('env', 'loggingLevel')
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger('my_ip')

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')
checkInterval = config.getint('IP_MONITOR', 'checkInterval')
telegram_token = config.get('IP_MONITOR', 'telegram-token')


def getMyPublicIP():
    ip = "199.203.68.10" if appMode == "dev" else getPublicIP()
    return ip;

def sendIP(publicIP):
    now =  datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")
    text = "Hello,\nPublic IP is " + str( publicIP) + "\nRaspberry PI time is " + now
    if(telegram_send_message(text, telegram_token)):
        return True
    else:
        return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI IP information",  appMode == "dev")
   

def bot_get_ip(bot, update):
    try:
        ip = getMyPublicIP()
        msg = "My public IP is: " + str(ip)
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get public IP: {0}".format(err))
   
def doCheckIP():
    lastPublicIP = None
    while True:
        try:
            publicIP = getMyPublicIP()
            logger.debug("Public IP: " + str(publicIP))
            if(publicIP !=lastPublicIP):	  
                sent = sendIP(publicIP)
                msg =  "Message with new public IP was sent" if sent else "Failed to send message with new public IP, will try to send later..."	
                logger.debug(msg)
                lastPublicIP = publicIP if sent else None   
        except Exception as err: 
            logger.critical("Failed to get public ip : {0}", format(err))
        time.sleep(checkInterval)            
    	
def exit_clean(signal=None, frame=None):
    logger.info("My IP monitoring stopping...")
    sys.exit(0)      
 
def main():	
    logger.info("My IP monitoring starting...")
    
    #wait few seconds for newtwork
    time.sleep(120)
    
    monitor_ip_thread = Thread(name='monitor_ip_thread', target=doCheckIP)
    monitor_ip_thread.daemon = True
    monitor_ip_thread.start()
   
    bot_commands = [("get", bot_get_ip, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token, 'commands': bot_commands})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()
    
    
    while True:
       #just sleep sometime
       time.sleep(60)

try:
    main()
except KeyboardInterrupt:
    exit_clean()
		
