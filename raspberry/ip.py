#!/usr/bin/env python3
from raspberry.gmail_utils import sendEmail
from raspberry.ip_utils import getPublicIP
import os, sys, configparser, time, logging, datetime
from threading import Thread
from raspberry.telegram_utils import is_logged_in
from raspberry.beacon import Beacon

logger = logging.getLogger('public-ip')

def getMyPublicIP():
    ip = getPublicIP()
    return ip;

def putBeacon(type,ip, beaconQueue):
    beacon = Beacon(type, ip, time.time() )
    beaconQueue.put(beacon)

def sendIP(publicIP, config, beaconQueue):
    sent = False
    if (config.getint('gmail', 'enable') == 1):
        gmailFromAddr = config.get('gmail', 'fromAddrs')
        gmailPassword= config.get('gmail', 'password')
        gmailToAddr = config.get('gmail', 'toAddrs')
        appMode = config.get('env', 'mode')
        now =  datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")
        text = "Hello,\nPublic IP is " + str( publicIP) + "\nRaspberry PI time is " + now
        sent  = sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI IP information",  appMode == "dev")
    
    if (config.getint('OPENHAB', 'enable') == 1):
        sent = True
    
    return sent    
   

def bot_get_ip(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    try:
        ip = getMyPublicIP()
        msg = "Public IP is: " + str(ip)
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get public IP: {0}".format(err))

         
def checkIP(config, beaconQueue):
    checkInterval = config.getint('IP_MONITOR', 'checkInterval')
    lastPublicIP = None
    while True:
        try:
            publicIP = getMyPublicIP()
            putBeacon(Beacon.TYPE_PUBLIC_IP, publicIP, beaconQueue)
        except Exception as err: 
            logger.critical("Failed to get public ip : {0}", format(err))
        time.sleep(checkInterval)            
    	