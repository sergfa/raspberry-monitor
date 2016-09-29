from raspberry.gmail_utils import sendEmail
import configparser
import time

config = configparser.ConfigParser()
config.read('env/config.cfg')
gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')

cpuThreshold = config.getint('TEMPERATURE_MONITOR', 'cpuThreshold')
gpuThreshold = config.getint('TEMPERATURE_MONITOR', 'gpuThreshold')
checkInterval = config.getint('TEMPERATURE_MONITOR', 'checkInterval')

def getCPUTemperature():
    return 60
	
def getGPUTemperature():
    return 60



def sendTemprature(cpuTemp, gpuTemp):
    text = "Hello,\n\nCPU temperature is " \
    + str( cpuTemp) + "\nGPU temperature is " +  str(gpuTemp)
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , text , "Raspberry PI Temperature Alert",  appMode == "dev")
   

   
def checkTemperature():
    cpuTemp = getCPUTemperature()
    gpuTemp = getGPUTemperature()
    print("CPU temperature: " + str(cpuTemp), ", GPU temperature: " + str(gpuTemp))
    if(cpuTemp >= cpuThreshold or gpuTemp >= gpuThreshold) :
        sent = sendTemprature(cpuTemp, gpuTemp);
        msg =  "Email was sent" if sent else "Failed to sent email"	
        print(msg)
    else:
        pass 
	
while True:
    checkTemperature()
    time.sleep(checkInterval)   
		