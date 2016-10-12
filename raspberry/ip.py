#!/usr/bin/env python3
from raspberry.gmail_utils import sendEmail
from raspberry.ip_utils import getPublicIP
import os, sys, configparser, time, logging, datetime
from threading import Thread
from raspberry.telegram_utils import is_logged_in

logger = logging.getLogger('ip')

def getMyPublicIP():
    ip = getPublicIP()
    return ip;

def sendIP(publicIP, config):
    gmailFromAddr = config.get('gmail', 'fromAddrs')
    gmailPassword= config.get('gmail', 'password')
    gmailToAddr = config.get('gmail', 'toAddrs')
    appMode = config.get('env', 'mode')
    now =  datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")
    text = "Hello,\nPublic IP is " + str( publicIP) + "\nRaspberry PI time is " + now
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI IP information",  appMode == "dev")
   

def bot_get_ip(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    try:
        ip = getMyPublicIP()
        msg = "Public IP is: " + str(ip)
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get public IP: {0}".format(err))

         
def checkIP(config):
    checkInterval = config.getint('IP_MONITOR', 'checkInterval')
    lastPublicIP = None
    while True:
        try:
            publicIP = getMyPublicIP()
            logger.debug("Public IP: " + str(publicIP))
            if(publicIP !=lastPublicIP):	  
                sent = sendIP(publicIP, config)
                msg =  "Message with new public IP was sent" if sent else "Failed to send message with new public IP, will try to send later..."	
                logger.debug(msg)
                lastPublicIP = publicIP if sent else None   
        except Exception as err: 
            logger.critical("Failed to get public ip : {0}", format(err))
        time.sleep(checkInterval)            
    	