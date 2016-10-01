#!/usr/bin/env python3

from raspberry.gmail_utils import sendEmail
import os, configparser, time, logging


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'config.cfg'))

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', 'presense.log')
loggingLevel =  config.get('env', 'loggingLevel')
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(message)s')

gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')

checkInterval = config.getint('PRESENSE_MONITOR', 'checkInterval')

logging.debug("Presense monitor module has been started")

presenseData = None;

def loadInitialPresenses():
    data = {}
    presenseFilename = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'presense.txt')
    with open(presenseFilename, "r") as lines:
        for line in lines:
            line = line.rstrip()
            person = line.split(None, 1);
            data[person[0]] = [person[1], -1]		
    return data

def checkPresense():
    logging.debug("checking presense")

def main():	
    presenseData = loadInitialPresenses();
    print(presenseData)
	
    while True:
        checkPresense()
        time.sleep(checkInterval)

try:
    main()
except:
    logging.critical("Unexpected error:", sys.exc_info()[0])
		
