#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.ip_utils import getPublicIP

import os, sys, configparser, time, logging, datetime
from threading import Thread
from raspberry.telegram_utils import telegram_bot


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
telegram_bot_password = config.get('TELEGRAM', 'bot-password')


def getMyPublicIP():
    ip = "199.203.68.10" if appMode == "dev" else getPublicIP()
    return ip;

def sendIP(publicIP):
    now =  datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")
    text = "Hello,\nPublic IP is " + str( publicIP) + "\nRaspberry PI time is " + now
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI IP information",  appMode == "dev")
   

def bot_get_ip(bot, update, args):
    if(len(args) < 1):
        update.message.reply_text('Sorry I can not send you data beacuse password is missing, use command /get <password>')
        return
    if(telegram_bot_password != args[0]):
        update.message.reply_text('Sorry I can not send you data beacuse password is incorrect.')
        return   
    try:
        ip = getMyPublicIP()
        msg = "Public IP is: " + str(ip)
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get public IP: {0}".format(err))
 
def bot_start(bot, update):
    update.message.reply_text('Hi! This is a private bot, you must have password to use it. Use /get <password> to get data')
 
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
    monitor_ip_thread = Thread(name='monitor_ip_thread', target=doCheckIP)
    monitor_ip_thread.daemon = True
    monitor_ip_thread.start()
   
    bot_commands = [("get", bot_get_ip, True), ("start", bot_start, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token, 'commands': bot_commands})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()

try:
    logger.info("My IP monitoring starting...")
    #wait few seconds for newtwork
    time.sleep(120)
    main()
    while True:
       #just sleep sometimes...
       time.sleep(60)

except KeyboardInterrupt:
    exit_clean()
		
