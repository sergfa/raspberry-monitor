#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
from raspberry.ip_utils import getPublicIP

import os, sys, configparser, time, logging, datetime


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'config.cfg'))

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', 'ip.log')
loggingLevel =  config.get('env', 'loggingLevel')
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(message)s')

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')
checkInterval = config.getint('IP_MONITOR', 'checkInterval')

logging.debug("My IP monitor module has been started")

lastPublicIP = None

def getMyPublicIP():
    ip = "199.203.68.10" if appMode == "dev" else getPublicIP()
    return ip;

def sendIP(publicIP):
    now =  datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")
    text = "Hello,\n\nPublic IP is " + str( publicIP) + "\n\nRaspberry PI time is " + now
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI IP information",  appMode == "dev")
   

   
def checkIP():
    global lastPublicIP
    publicIP = None
    try:
	    publicIP = getMyPublicIP()
    except: 
        logging.critical("Failed to get public ip", sys.exc_info()[0])	
        return
		
    logging.debug("Public IP: " + str(publicIP))
    if(publicIP !=lastPublicIP) :
        lastPublicIP = publicIP	  
        sent = sendIP(publicIP);
        msg =  "Email was sent" if sent else "Failed to sent email"	
        logging.debug(msg)
    else:
        pass 

def main():	
    time.sleep(60)    
    while True:
        checkIP()
        time.sleep(checkInterval)

try:
    main()
except:
    logging.critical("Unexpected error:", sys.exc_info()[0])
		
