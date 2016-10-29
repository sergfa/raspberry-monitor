#!/usr/bin/env python3
from raspberry.temperature_utils import getCpuTemperature
from raspberry.temperature_utils import getGpuTemperature
from raspberry.telegram_utils import is_logged_in
import os, sys, time, logging
from raspberry.beacon import Beacon

logger = logging.getLogger('rpi-temperature')

def getCpuTemp():
    temp = getCpuTemperature()
    return temp
	
def getGpuTemp():
    temp = getGpuTemperature()
    return temp

def putBeacon(key, type,cpuTemp, beaconQueue):
    beacon = Beacon(key, type, cpuTemp, time.time() )
    beaconQueue.put(beacon)
       
def checkTemp(beaconQueue, checkInterval):
    
    while True:
        cpuTemp = getCpuTemp()
        gpuTemp = getGpuTemp()
        logger.debug("Current CPU temperature: " + str(cpuTemp) + ", GPU temperature: " + str(gpuTemp))
        putBeacon(Beacon.KEY_CPU_TEMPERATURE(), Beacon.TYPE_TEMPERATURE(), cpuTemp, beaconQueue);
        putBeacon(Beacon.KEY_GPU_TEMPERATURE(), Beacon.TYPE_TEMPERATURE(), gpuTemp, beaconQueue);
        time.sleep(checkInterval)    
        
def bot_get_temperature(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    cpuTemp = getCpuTemp()
    gpuTemp = getGpuTemp()
    msg = "CPU temperature is: " + str(cpuTemp) + ", GPU temperature is: " + str(gpuTemp)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    
		
